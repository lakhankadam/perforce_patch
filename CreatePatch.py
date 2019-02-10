import subprocess
import os
import sys

class CreatePatch():

    def create_patch(self,changelist,name):
            
            output = subprocess.check_output(["p4", "describe" ,"-s",changelist])

            if "edit" not in output and "add" not in output:
                print "The changelist "+ changelist + " is shelved. Please unshelve it and run the script again..."
                return

            depot_files = subprocess.check_output(["p4","client","-o"])
            depot_files = depot_files.split("View:")[3].replace("\n","").replace("\t","").split("/...")[:-1]
            depot_map = dict()
            for i in range(len(depot_files)/2):
                if depot_files[i] not in depot_map:
                    depot_map[depot_files[i].replace("//","")] = depot_files[2*i+1].replace("//","").strip()

            output = output.split("\n")
            files = []
            for file in output:
                if file.startswith("... "):
                    file = file.replace("... ","")
                    files.append(file.split(" ")[0])

            user = subprocess.check_output(["whoami"]).replace("\n","")

            doc_path = "/home/"+user+"/Documents"

            for file in files:
                for key in depot_map:
                    if key in file:
                        file = file.replace("//","")
                        file_name = file.split("/")[-1]
                        folder_name = "/".join(file.split("/")[:-1])
                        # print folder_name
                        os.chdir(doc_path)
                        subprocess.check_output(["mkdir","-p",folder_name])
                        os.chdir(folder_name)
                        file = file.replace(key,"/sandbox/"+depot_map[key])
                        zip_folder = key.split("/")[0]
                        subprocess.check_output(["touch",file_name])
                        subprocess.check_output(["cp",file.split("#")[0],file_name])
            os.chdir(doc_path)
            print subprocess.check_output(["zip","-r",name+".zip",zip_folder])
            subprocess.check_output(["rm","-rf",zip_folder])
            print "The zip folder " +zip_folder+ " is present in Documents"


if __name__ == '__main__':
    cpatch = CreatePatch()

    if len(sys.argv) != 3:
        print "No of arguments insufficient. Enter changelist number followed by name of zip folder"
    else:
        cpatch.create_patch(str(sys.argv[1]),str(sys.argv[2]))