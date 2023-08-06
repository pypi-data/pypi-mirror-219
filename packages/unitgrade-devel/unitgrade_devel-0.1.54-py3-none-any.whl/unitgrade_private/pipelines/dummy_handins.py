import os.path
import os
import shutil
import numpy as np
import glob
import subprocess

def make_dummies(zip_file_path="zip1.zip", n_handins=3, screwups=4, student_base_dir=None, student_grade_file=None, instructor_base_dir=None):
    # I am dum-dum.
    dir = os.path.dirname(__file__)
    tmp = dir + "/tmp"
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    # now we got a temp dir.
    # Deploy to this dir and create handins. Turn it all into a .zip file and return it.
    np.random.seed(42)

    def copy_and_mutate():
        if os.path.isdir(tmp + "/students"):
            shutil.rmtree(tmp + "/students")


        shutil.copytree(student_base_dir, tmp + "/students",dirs_exist_ok=True)
        # Copy instructor files over and mutate.
        for file in glob.glob(student_base_dir +"/**/*.py"):
            # print(file)

            rel = os.path.relpath(file, student_base_dir)
            with open(tmp +"/students/"+rel, 'r') as f:
                st_f = f.read()

            with open(instructor_base_dir + "/"+os.path.relpath(file, student_base_dir), 'r') as f:
                in_f = f.read()

            from snipper.block_parsing import indent

            if st_f == in_f:
                continue
            else:
                # Take the instructor version and mutate it.
                print("Messing up file", file)
                in_mut = []
                from snipper.block_parsing import indent
                in_f_split =in_f.splitlines()
                for k, l in enumerate(in_f_split):


                    if k > 0 and len(indent(l)) > 0 and indent(l) == indent(in_f_split[k-1]):
                        if np.random.rand() < 0.1:
                            in_mut.append(indent(l) +"assert(False)")
                    in_mut.append(l)

                # "\n".join(in_mut)
                with open(tmp + "/students/" + rel, 'w') as f:
                    f.write("\n".join(in_mut))


        module = ".".join(os.path.relpath(student_grade_file, student_base_dir)[:-3].split("/"))
        cmd = f"cd {tmp}/students && python -m {module}"
        print(cmd)
        o = subprocess.run(cmd, shell=True, capture_output=True, check=True)
        print(o)


        token = glob.glob(os.path.dirname(tmp +"/students/"+os.path.relpath(student_grade_file, student_base_dir)) + "/*.token")[0]
        print(token)
        return token

    names = ['Alice', 'Bob', 'Charlie', 'Doris', 'Ebert']

    # def zipfolder(foldername, target_dir):
    #     zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    #     rootlen = len(target_dir) + 1
    #     for base, dirs, files in os.walk(target_dir):
    #         for file in files:
    #             fn = os.path.join(base, file)
    #             zipobj.write(fn, fn[rootlen:])



    for k in range(n_handins):
        token = copy_and_mutate()

        # Now make directory for handin and create the .zip file.

        id = 221000 + k
        handin_folder = f"116607-35260 - s{id} - {names[k % len(names)]} - 1 March, 2022 518 PM"
        os.makedirs(tmp + "/zip/"+handin_folder)

        shutil.copy(token, tmp + "/zip/"+handin_folder +"/"+os.path.basename(token))

    shutil.make_archive(zip_file_path[:-4],
                        'zip',
                        tmp+ "/zip",
                        '')

    return zip_file_path


    # zipfolder('zip1', tmp + "/zip/"+handin_folder)  # insert your variables here
    # sys.exit()

    #
    # import zipfile
    #
    # with zipfile.ZipFile(zip_file_path, 'w') as zip:
    #     zip.
    #
    #
    # a = 234
    # pass