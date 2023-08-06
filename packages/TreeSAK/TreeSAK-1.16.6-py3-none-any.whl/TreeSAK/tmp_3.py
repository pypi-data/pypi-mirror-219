import os


def group_marker(taxa_counts_tats_op_txt, marker_seq_dir, op_dir, force_overwrite):

    # define file name
    marker_set_top_25_txt       = '%s/top25.txt'    % op_dir
    marker_set_top_50_txt       = '%s/top50.txt'    % op_dir
    marker_set_top_75_txt       = '%s/top75.txt'    % op_dir
    marker_set_top_100_txt      = '%s/top100.txt'   % op_dir
    marker_set_top_25_seq_dir   = '%s/top25'        % op_dir
    marker_set_top_50_seq_dir   = '%s/top50'        % op_dir
    marker_set_top_75_seq_dir   = '%s/top75'        % op_dir
    marker_set_top_100_seq_dir  = '%s/top100'       % op_dir

    # create output folder
    if os.path.isdir(op_dir) is True:
        if force_overwrite is True:
            os.system('rm -r %s' % op_dir)
        else:
            print('%s already exist, program exited!' % op_dir)
            exit()

    os.system('mkdir %s' % op_dir)
    os.system('mkdir %s' % marker_set_top_25_seq_dir)
    os.system('mkdir %s' % marker_set_top_50_seq_dir)
    os.system('mkdir %s' % marker_set_top_75_seq_dir)
    os.system('mkdir %s' % marker_set_top_100_seq_dir)

    marker_set_top_25 = set()
    marker_set_top_50 = set()
    marker_set_top_75 = set()
    marker_set_top_100 = set()
    header_index_dict = {}
    for each_marker in open(taxa_counts_tats_op_txt):
        each_marker_split = each_marker.replace('\n', '').split('\t')
        if each_marker.startswith('MarkerID\t'):
            header_index_dict = {k: v for v, k in enumerate(each_marker_split)}
        else:
            marker_id = each_marker_split[header_index_dict['MarkerID']]
            best_25perc = each_marker_split[header_index_dict['best_25perc']]
            best_50perc = each_marker_split[header_index_dict['best_50perc']]
            worst_50perc = each_marker_split[header_index_dict['worst_50perc']]
            worst_25perc = each_marker_split[header_index_dict['worst_25perc']]
            if best_25perc != '':
                marker_set_top_25.add(marker_id)
                os.system('cp %s/%s.fa %s/' % (marker_seq_dir, marker_id, marker_set_top_25_seq_dir))
            if best_50perc != '':
                marker_set_top_50.add(marker_id)
                os.system('cp %s/%s.fa %s/' % (marker_seq_dir, marker_id, marker_set_top_50_seq_dir))
            if worst_25perc == '':
                marker_set_top_75.add(marker_id)
                os.system('cp %s/%s.fa %s/' % (marker_seq_dir, marker_id, marker_set_top_75_seq_dir))
            marker_set_top_100.add(marker_id)
            os.system('cp %s/%s.fa %s/' % (marker_seq_dir, marker_id, marker_set_top_100_seq_dir))

    with open(marker_set_top_25_txt, 'w') as marker_set_top_25_txt_handle:
        marker_set_top_25_txt_handle.write('\n'.join(sorted([i for i in marker_set_top_25])))
    with open(marker_set_top_50_txt, 'w') as marker_set_top_50_txt_handle:
        marker_set_top_50_txt_handle.write('\n'.join(sorted([i for i in marker_set_top_50])))
    with open(marker_set_top_75_txt, 'w') as marker_set_top_75_txt_handle:
        marker_set_top_75_txt_handle.write('\n'.join(sorted([i for i in marker_set_top_75])))
    with open(marker_set_top_100_txt, 'w') as marker_set_top_100_txt_handle:
        marker_set_top_100_txt_handle.write('\n'.join(sorted([i for i in marker_set_top_100])))


taxa_counts_tats_op_txt = '/Users/songweizhi/Desktop/test_current/TaxaCountStats_wd/TaxaCountStats_output.txt'
marker_seq_dir          = '/Users/songweizhi/Documents/Research/Sponge_Hologenome/5_OMA_wd_r214/Output/OrthologousGroupsFasta'
force_overwrite         = True
op_dir                  = '/Users/songweizhi/Desktop/test_current/TaxaCountStats_wd/TaxaCountStats_output'

group_marker(taxa_counts_tats_op_txt, marker_seq_dir, op_dir, force_overwrite)
