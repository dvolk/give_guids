
import glob, uuid, json, pathlib, time, shutil

def get_sample_paths(pattern):
	return glob.glob(pattern)

def get_sample_filename(file_path):
        return pathlib.Path(file_path).name

def get_sample_directory(file_path):
	return pathlib.Path(file_path).parent

#
# assumes that sample name ends at the first _ character
#
def get_sample_name(file_path):
	xs = get_sample_filename(file_path).split("_")
	return xs[0], xs[1:]

def is_filename_already_a_guid(file_path):
	name = get_sample_name(file_path)
	try:
		eh = uuid.UUID(name)
	except:
		return False
	return True

#
# this renames all files matching a sample name to a single guid
#
# 1. get the sample name following {PATTERN}/{SAMPLE_NAME}{SUFFIX} pattern
#
# 2. generate {GUID}
#
# 3. rename all files matching {PATTERN}/{SAMPLE_NAME}* to {GUID}{SUFFIX}
#
# 4. output json array to stdout that can be used by import.py
#
def main():
	time_now = time.gmtime()

	suffix = "_consensus.fasta.gz"
	pattern = "/mnt/disk2/output/*/projects/CompassCloud/run_ncbi500-2/BaseCall/*{0}".format(suffix)

	dict_out = []
	paths = get_sample_paths(pattern)

	for path in paths:
		if is_filename_already_a_guid(path):
#			print("path filename {0} is already a guid".format(path))
			continue

		name,_ = get_sample_name(path)
		guid = str(uuid.uuid4())
		directory = get_sample_directory(path)

		filename = get_sample_filename(path)
		new_filename = guid + suffix
		new_path = get_sample_directory(path) / pathlib.Path(new_filename)

#		pathlib.Path(path).rename(new_path)
#		print("renaming file {0} to\n              {1}".format(path, new_path))

		sample_dict = dict()
		sample_dict['associated_files'] = []

		associated_files = glob.glob(str(directory / name) + "*")
		for associated_file in associated_files:
			name_ = name
#			name_,_ = get_sample_name(associated_file)
			filename_ = get_sample_filename(associated_file)
			suffix_ = filename_[len(name_):]
			new_path_ = directory / "{0}{1}".format(guid, suffix_)
#			print("renaming file {0} to\n              {1}".format(associated_file, new_path_))
			pathlib.Path(associated_file).rename(new_path_)
			sample_dict['associated_files'].append("{0}{1}".format(name_, suffix_))

		sample_dict['path'] = str(new_path)
		sample_dict['guid'] = guid
		sample_dict['sample_name'] = name
		sample_dict['file_name'] = new_filename
		sample_dict['directory'] = str(directory)
		sample_dict['time_added_epoch'] = time.strftime("%s", time_now)
		sample_dict['additional_data'] = {}
		sample_dict['additional_data']["give_guids.py"] = "converted with give_guids.py"

		dict_out.append(sample_dict)

	print(json.dumps(dict_out))

if __name__ == "__main__":
	main()
