import os, csv, sys

# Function to generate frameMD5 from input file
def gen_framemd5(file):
    os.system(f'ffmpeg -i {file}  -f framemd5 {file[:-4]}_{file[-3:]}.framemd5')
    
    return os.path.join(source_dir, f'{file[:-4]}_{file[-3:]}.framemd5')


# Function to transcode source file to FFV1/MKV
def transcode_to_mkv(file):
    os.system(f'ffmpeg -i {file} -level 3  -coder 1 -g 1 -c:v ffv1 {file[:-4]}.mkv')

    return(os.path.join(source_dir, f'{file[:-4]}.mkv'))

    
# Function to compare the Frame MD5 files and save results in CSV
def compare_frameMD5_files(*argv):
    with open('frameMD5_compare.csv' ,'w',  newline='\n') as frameMD5_csv:
        writer = csv.writer(frameMD5_csv, delimiter=',')

        # Feteches frameMD5 file and returns it as iterable list
        def _fetch(frame_md5_file):
            with open(frame_md5_file ,'r') as frame_md5:
                return frame_md5.readlines()

        # Iterates over both frameMD5 files simultaneously and comapres checksums, writes result to CSV file
        for a, b in zip(_fetch(argv[0][0]), _fetch(argv[0][1])):
            if a != b:
                writer.writerow([a.strip()[47:], b.strip()[47:], 'ERROR'])
                print(a.strip()[47:], b.strip()[47:])
            else:
                writer.writerow([a.strip()[47:], b.strip()[47:], 'PASS'])



# Main function: Creates F-MD5 of source file, transcodes to FFV1, generates F-MD5 of new FFV1, then compares and saves result
def main():
    os.chdir(source_dir)
    for file in os.listdir(os.getcwd()):
        if file[-3:] in ['avi', 'mov']:
            gen_framemd5(file)
            transcode_to_mkv(file)

    for file in os.listdir(os.getcwd()):
        if file[-3:] == 'mkv':
            gen_framemd5(file)
    
    compare_frameMD5_files([os.path.join(source_dir, file) for file in os.listdir(source_dir) if file.endswith('.framemd5')])


if __name__ == '__main__':
    source_dir = os.path.normpath(input('Paste folder directory '))
    main()
