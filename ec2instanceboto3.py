import boto3
ec2_resource = boto3.resource('ec2') #we need to add the name of AWS service EC2

#we add all the information related to EC2 instance
instances = ec2_resource.create_instances(
    ImageId = 'ami-0850ab57897dcaa32',
    MinCount = 1, #number of instances
    MaxCount = 1, # number of instances
    InstanceType = 't2.micro', # instance type
    KeyName = 'instcopy1', #this is the key pair
    SecurityGroupIds=["sg-093c18ac4444e9fb1","sg-b84fdfd9"],
    BlockDeviceMappings = [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 20,  # 20 GB root volume
                'VolumeType': 'gp2',  # General Purpose SSD
                'DeleteOnTermination': False
            }
        }
    ],
    UserData='''#!/bin/bash
    # Update the package list
    sudo apt update -y
    # Install Apache
    sudo apt install apache2 -y
    # Start Apache service
    sudo systemctl start apache2
    # Enable Apache to start on boot
    sudo systemctl enable apache2
    # Create a sample index.html
    echo "<html><body><h1>Welcome to Apache Web Server - Shikhar Verma</h1></body></html>" | sudo tee /var/www/html/index.html
    # Adjust the firewall (if required)
    sudo ufw allow 'Apache'
    ''',
    TagSpecifications = [ #tagging is very useful to identify the instance on AWS
        {                 #After creating the tagging we are good to run the script
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name', 
                    'Value': 'Pythontest' # name of the EC2 instance name
                },
                {
                    'Key': 'Department',
                    'Value': 'Technical',
                },
                {
                    'Key': 'Environment',
                    'Value': 'Test'
                }
            ]
        }
    ]
)

# Print instance details
for instance in instances:
    print(f'Instance {instance.id} launched with a 20GB volume and HTTP server.')
