import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def create_degree_df(degree_df, followings):
    extract_degree_df = degree_df[['id', 'name', 'out_degree',
                                   'in_degree', 'degree', 'followers_count', 'friends_count']].copy()
    extract_degree_df['follower_of_hsd'] = extract_degree_df.apply(
        lambda row: is_follower_of(followings, row, 3063800235), axis=1)
    extract_degree_df['friend_of_hsd'] = extract_degree_df.apply(
        lambda row: is_friend_of(followings, row, 3063800235), axis=1)
    return extract_degree_df


def is_follower_of(followings, user, hs_id):
    return not(followings[(followings['id'] == user['id']) & (followings['follower_of'] == hs_id)].empty)


def is_friend_of(followings, user, hs_id):
    return not(followings[(followings['id'] == hs_id) & (followings['follower_of'] == user['id'])].empty)


def get_num_of_followed_hs_by_user(followings, user, hs_ids):
    return followings[(followings['id'] == user['id']) & (followings['follower_of'].isin(hs_ids))].shape[0]


def get_num_of_hs_following_user(followings, user, hs_ids):
    return followings[(followings['follower_of'] == user['id']) & (followings['id'].isin(hs_ids))].shape[0]


def create_additional_info_cols(df, followings, hs_ids):
    df['num_followed_hs'] = df.apply(lambda row: get_num_of_followed_hs_by_user(
        followings, row, hs_ids), axis=1)
    df['num_following_hs'] = df.apply(lambda row: get_num_of_hs_following_user(
        followings, row, hs_ids), axis=1)


def create_follower_friend_cols(df, followings, hs_ids):
    df['follower_of_hsd'] = df.apply(
        lambda row: is_follower_of(followings, row, 3063800235), axis=1)
    df['friend_of_hsd'] = df.apply(
        lambda row: is_friend_of(followings, row, 3063800235), axis=1)
    df['follower_of_rwth'] = df.apply(
        lambda row: is_follower_of(followings, row, 928008620), axis=1)
    df['friend_of_rwth'] = df.apply(
        lambda row: is_friend_of(followings, row, 928008620), axis=1)
    df['follower_of_koeln'] = df.apply(
        lambda row: is_follower_of(followings, row, 11053712), axis=1)
    df['friend_of_koeln'] = df.apply(
        lambda row: is_friend_of(followings, row, 11053712), axis=1)
    df['follower_of_muenster'] = df.apply(
        lambda row: is_follower_of(followings, row, 84606793), axis=1)
    df['friend_of_muenster'] = df.apply(
        lambda row: is_friend_of(followings, row, 84606793), axis=1)
    df['follower_of_rhein_waal'] = df.apply(
        lambda row: is_follower_of(followings, row, 265859722), axis=1)
    df['friend_of_rhein_waal'] = df.apply(
        lambda row: is_friend_of(followings, row, 265859722), axis=1)
    df['follower_of_niederrhein'] = df.apply(
        lambda row: is_follower_of(followings, row, 2776187059), axis=1)
    df['friend_of_niederrhein'] = df.apply(
        lambda row: is_friend_of(followings, row, 2776187059), axis=1)
    df['follower_of_dortmund'] = df.apply(
        lambda row: is_follower_of(followings, row, 103823788), axis=1)
    df['friend_of_dortmund'] = df.apply(
        lambda row: is_friend_of(followings, row, 103823788), axis=1)
    df['follower_of_bochum'] = df.apply(
        lambda row: is_follower_of(followings, row, 124155166), axis=1)
    df['friend_of_bochum'] = df.apply(
        lambda row: is_friend_of(followings, row, 124155166), axis=1)


def get_followed_hs_by_user(followings, users, user_id, hs_ids):
    ids = list(followings[(followings['id'] == user_id) & (
        followings['follower_of'].isin(hs_ids))]['follower_of'])
    names_df = users[users['id'].isin(ids)]
    return names_df.loc[:, ['id', 'name', 'followers_count']]


def get_hs_following_user(followings, users, user_id, hs_ids):
    ids = list(followings[(followings['follower_of'] == user_id) & (
        followings['id'].isin(hs_ids))]['id'])
    names_df = users[users['id'].isin(ids)]
    return names_df.loc[:, ['id', 'name', 'followers_count']]


def get_overlap_percentages(overall_values, hs_dict):
    index = 0
    overlap_percentages = []
    for name_lvl1, values_lvl1 in hs_dict.items():
        overlap_count = set()
        for name_lvl2, values_lvl2 in hs_dict.items():
            if (not(name_lvl1 == name_lvl2)):
                overlap_count.update(
                    frozenset(values_lvl1[values_lvl1.isin(values_lvl2)]))
        total_overlap_perc = round(
            (len(overlap_count) / overall_values[index]) * 100, 2)
        overlap_percentages.append(total_overlap_perc)
        print(name_lvl1 + ": " + str(len(overlap_count)) +
              " (" + str(total_overlap_perc) + "%)")
        index = index + 1

    return overlap_percentages


def get_overlap_matrix(hs_dict):
    hochschulen_counts = []
    for name_lvl1, list_lvl1 in hs_dict.items():
        overlap_percentages = []
        for name_lvl2, list_lvl2 in hs_dict.items():
            if (not(name_lvl1 == name_lvl2)):
                # get overlapping followers for every hs
                overlap_count = list_lvl1[list_lvl1.isin(list_lvl2)].count()
                # get total unique follower of both hs
                total_follower = list_lvl1.count() + list_lvl2.count() - overlap_count
                overlap_percent = round(
                    (100 / total_follower) * overlap_count, 1)
                overlap_percentages.append(overlap_percent)
            else:
                overlap_percentages.append(0)
        hochschulen_counts.append(overlap_percentages)
    return hochschulen_counts


def create_hs_heat_map(hs_dict, title):
    hs_names = hs_dict.keys()
    hs_counts = get_overlap_matrix(hs_dict)

    data = np.array(hs_counts)

    mask = np.tri(data.shape[0], k=0)
    data = np.ma.array(data, mask=mask).T

    fig, ax = plt.subplots(figsize=(20, 8))
    im = ax.imshow(data, cmap='viridis')

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(hs_names)), labels=hs_names)
    ax.set_yticks(np.arange(len(hs_names)), labels=hs_names)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(hs_names)):
        for j in range(len(hs_names)):
            text_color = "white"
            if data[i, j] > 7:
                text_color = "black"
            else:
                text_color = "white"

            label = str(data[i, j]) + " %"

            text = ax.text(j, i, label,
                           ha="center", va="center", color=text_color)

    ax.set_title(title)
    plt.show()


def create_bar_plot_for_hs(hochschulen, values, y_label, title, center):
    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(hochschulen, values, color='maroon',
            width=0.4)

    height = (sum(values) / len(values)) * 0.03

    for i in range(len(values)):
        plt.text(i - center, values[i] + height, int(values[i]))

    plt.xticks(rotation=30, ha='right')

    plt.xlabel("Hochschulen")
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def create_centralities(G):
    for i in sorted(G.nodes()):
        G.nodes[i]['degree'] = G.degree()(i)
        G.nodes[i]['out_degree'] = G.out_degree()(i)
        G.nodes[i]['in_degree'] = G.in_degree()(i)

    # extraction of network nodes in a dataframe
    nodes_data = pd.DataFrame([i[1] for i in G.nodes(data=True)], index=[
                              i[0] for i in G.nodes(data=True)])
    nodes_data = nodes_data.sort_values(by='out_degree', ascending=False)
    nodes_data.index.names = ['id']
    nodes_data.reset_index(level=0, inplace=True)

    # Betweenness centrality
    bet_cen = nx.betweenness_centrality(G)
    df_bet_cen = pd.DataFrame.from_dict(bet_cen, orient='index')
    df_bet_cen.columns = ['betweenness_centrality']
    df_bet_cen.index.names = ['id']
    df_bet_cen.reset_index(level=0, inplace=True)
    analyse = pd.merge(nodes_data, df_bet_cen, on=['id'])

    # Closeness centrality
    clo_cen = nx.closeness_centrality(G)
    df_clo = pd.DataFrame.from_dict(clo_cen, orient='index')
    df_clo.columns = ['closeness_centrality']
    df_clo.index.names = ['id']
    df_clo.reset_index(level=0, inplace=True)
    analyse = pd.merge(analyse, df_clo, on=['id'])

    # Eigenvector centrality
    eig_cen = nx.eigenvector_centrality_numpy(G)
    df_eig = pd.DataFrame.from_dict(eig_cen, orient='index')
    df_eig.columns = ['eigenvector_centrality']
    df_eig.index.names = ['id']
    df_eig.reset_index(level=0, inplace=True)
    analyse = pd.merge(analyse, df_eig, on=['id'])

    return analyse
