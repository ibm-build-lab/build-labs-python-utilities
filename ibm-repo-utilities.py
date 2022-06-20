# -----------------------------------------------------------------------------------------------------------
# Login to the IBM repository via command line prior to running this application.  The local re-tagged images
# will be deleted.
#
# IBM Cloud Repostiory Login Commands
# ibmcloud login -a https://cloud.ibm.com -u passcode -p JGpdPdkn19  (Cloud Login)
# ibmcloud target -g sandbox-rg (Resource Group Targetting)
# ibmcloud cr login (IBM Repository Login)
# ibmcloud cr region-set us-south (IBM Repository Region Targetting)
#-----------------------------------------------------------------------------------------------------------

import subprocess, json
aws_repository_filter = '228078468156.dkr.ecr.us-east-2.amazonaws.com/5gc'
aws_repository = '228078468156.dkr.ecr.us-east-2.amazonaws.com'
container_version = '7.1.1'
ibm_repository = 'us.icr.io'

def getDockerImageNames():
    image_list = []
    p = subprocess.Popen('docker image ls --format "{{json . }}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        repo_name = json.loads(line.strip().decode('utf-8'))
        image_list.append(repo_name)
    retval = p.wait()
    return image_list

def main():
    mod_image_name = ""
    local_image_list = getDockerImageNames()
    for image_name in local_image_list:
        if (aws_repository in image_name['Repository'] and container_version in image_name['Tag']):
            # Re-tag images
            # Process repository name - IBM Repo does not support 3 character first level repository names
            old_tag_name = image_name['Repository'] + ':' + image_name['Tag']
            mod_tag_name = image_name['Repository'].replace(aws_repository, ibm_repository, 1)
            new_tag_name = mod_tag_name.replace("/5gc/", "/casa-5gc/", 1) + ':' + image_name['Tag']

            # print(old_tag_name, new_tag_name)
            docker_cmd = 'docker tag ' + old_tag_name + ' ' + new_tag_name
            print(docker_cmd)
            p = subprocess.Popen(docker_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                print(line.strip().decode('utf-8'))
            retval = p.wait()

            # Push images to IBM Repo
            p = subprocess.Popen('docker push ' + new_tag_name, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
                print(line.strip().decode('utf-8'))
            retval = p.wait()

if __name__ == "__main__":
    main()
