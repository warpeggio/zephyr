import base64
import os
import pulumi
import pulumi_eks as eks
import pulumi_aws as aws
import pulumi_kubernetes as k8s
import pulumi_docker as docker

cluster_name = "zephyr-cluster"
cluster_tag = f"kubernetes.io/cluster/{cluster_name}"

public_subnet_cidrs = ["172.31.0.0/20", "172.31.48.0/20"]

# Use 2 AZs for our cluster
avail_zones = ["us-east-1a", "us-east-1b"]

# Create VPC for EKS Cluster
vpc = aws.ec2.Vpc(
	"eks-vpc",
	cidr_block="172.31.0.0/16"
)

igw = aws.ec2.InternetGateway(
	"eks-igw",
	vpc_id=vpc.id,
)

route_table = aws.ec2.RouteTable(
	"eks-route-table",
	vpc_id=vpc.id,
	routes=[
		{
			"cidr_block": "0.0.0.0/0",
			"gateway_id": igw.id
		}
	]
)

public_subnet_ids = []

# Create public subnets that will be used for the AWS Load Balancer Controller
for zone, public_subnet_cidr  in zip(avail_zones, public_subnet_cidrs):
    public_subnet = aws.ec2.Subnet(
        f"eks-public-subnet-{zone}",
        assign_ipv6_address_on_creation=False,
        vpc_id=vpc.id,
        map_public_ip_on_launch=True,
        cidr_block=public_subnet_cidr,
        availability_zone=zone,
        tags={
	     			# Custom tags for subnets
            "Name": f"eks-public-subnet-{zone}",
            cluster_tag: "owned",
            "kubernetes.io/role/elb": "1",
        }
    )

    aws.ec2.RouteTableAssociation(
        f"eks-public-rta-{zone}",
        route_table_id=route_table.id,
        subnet_id=public_subnet.id,
    )
    public_subnet_ids.append(public_subnet.id)

# Create an EKS cluster.
cluster = eks.Cluster(
    cluster_name,
		name=cluster_name,
    vpc_id=vpc.id,
    instance_type="t2.medium",
    desired_capacity=2,
    min_size=1,
    max_size=2,
    #provider_credential_opts=kube_config_opts,
    public_subnet_ids=public_subnet_ids,
    create_oidc_provider=True,
)

# Export the cluster's kubeconfig.
pulumi.export("kubeconfig", cluster.kubeconfig)

#=====================================================================================================
# setting up the ECR
ecr_repo = aws.ecr.Repository("zephyr-ecr-repo")

repo_policy = aws.ecr.RepositoryPolicy(
    "zephyr-ecr-repo-policy",
    policy="""{
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "new policy",
                "Effect": "Allow",
                "Principal": "*",
                "Action": [
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "ecr:InitiateLayerUpload",
                    "ecr:UploadLayerPart",
                    "ecr:CompleteLayerUpload",
                    "ecr:DescribeRepositories",
                    "ecr:GetRepositoryPolicy",
                    "ecr:ListImages",
                    "ecr:DeleteRepository",
                    "ecr:BatchDeleteImage",
                    "ecr:SetRepositoryPolicy",
                    "ecr:DeleteRepositoryPolicy"
                ]
            }
        ]
    }""",
    repository=ecr_repo.name
)

ecr_access_policy = aws.iam.Policy(
    "ecr-access-iam-policy",
    policy="""{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetAuthorizationToken"
          ],
          "Resource": "*"
        }
      ]
    }"""
)

nodeInstanceRole = aws.iam.RolePolicyAttachment(
    "eks-NodeInstanceRole-policy-attach",
    role=cluster.instance_roles[0].name,
    policy_arn=ecr_access_policy.arn,
)

pulumi.export("ecr_repo_url", ecr_repo.repository_url)

# Get registry info (creds and endpoint).
def getRegistryInfo(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])
image_name = ecr_repo.repository_url
registry_info = ecr_repo.registry_id.apply(getRegistryInfo)

image = docker.Image('zephyr-image',
    build='../',
    image_name=image_name,
    registry=registry_info,
)

# Export the base and specific version image name.
pulumi.export('baseImageName', image.base_image_name)
pulumi.export('fullImageName', image.image_name)


#=====================================================================================================
# Final section: Load the image into the kubernetes cluster
eks_provider = k8s.Provider("eks-provider", kubeconfig=cluster.kubeconfig_json)
app_labels = { 'app': 'zephyr-webapp' }
app_dep = k8s.apps.v1.Deployment('zephyr-dep',
    spec={
        'selector': { 'matchLabels': app_labels },
        'replicas': 3,
        'template': {
            'metadata': { 'labels': app_labels },
            'spec': {
                'containers': [{
                    'name': 'zephyr-webapp',
                    'image': image.image_name,
                }],
            },
        },
    },
    opts=pulumi.ResourceOptions(provider=eks_provider)
)
app_svc = k8s.core.v1.Service('zephyr-svc',
    metadata={ 'labels': app_labels },
    spec={
        'type': 'LoadBalancer',
        'ports': [{ 'port': 80, 'targetPort': 5000, 'protocol': 'TCP' }],
        'selector': app_labels,
    },
    opts=pulumi.ResourceOptions(provider=eks_provider)
)
#pulumi.export('appIp', app_svc.status.apply(lambda s: s.loadBalancer.ingress[0].hostname))
pulumi.export("appUrl", app_svc.status.load_balancer.ingress[0].hostname)

