import tdtools as tdt
import h5py


class BasicRun:
    def __init__(self, data, tag_dict):
        self.tags = tag_dict
        self.data = data


class RunFromFile(BasicRun):
    def __init__(self, file_name, tag_dict, rot_offset=0, num_frames=0):
        super().__init__(tdt.get_territory_data(file_name, rot_offset, num_frames), tag_dict)


class ComputeRun(BasicRun):
    def __init__(self, run_obj, func, *args):
        super().__init__(func(run_obj.data, *args), run_obj.tags)


class BasicExp:
    def __init__(self, runs):
        self.runs = runs

    def compute_across_runs(self, func, *args):
        run_list = []
        for r in self.runs:
            run_list.append(ComputeRun(r, func, *args))
        self.runs = run_list

    def compute_across_groups(self, key_name, func, *args):
        group_out = dict()
        group_ids = self.unique_key_vals(key_name)
        for g in group_ids:
            group_runs = self.get_runs_from_tag(key_name, g)
            group_data, group_info = self.get_group_data_info(group_runs)
            group_out[g] = func(g, group_data, group_info, *args)
        return group_out

    def compute_across_group(self, key_name, tag_name, func, *args):
        group_out = dict()
        group_runs = self.get_runs_from_tag(key_name, tag_name)
        group_data, group_info = self.get_group_data_info(group_runs)
        group_out = func(tag_name, group_data, group_info, *args)
        return group_out

    def unique_key_vals(self, key_name):
        unique_tags = []
        for r in self.runs:
            val = r.tags[key_name]
            if val not in unique_tags:
                unique_tags.append(val)
        return unique_tags

    def get_runs_from_tag(self, key_name, tag_name):
        tagged_runs = []
        for r in self.runs:
            if r.tags[key_name] is tag_name:
                tagged_runs.append(r)
        return tagged_runs

    def get_group_data_info(self, group_runs):
        group_data = []
        group_info = []
        for r in group_runs:
            group_data.append(r.data)
            group_info.append(r.tags)
        return group_data, group_info
