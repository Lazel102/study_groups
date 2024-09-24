import pandas as pd
import numpy as np
from itertools import combinations
from itertools import product

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['disciplines'] = data['disciplines'].apply(lambda x: x.split(', '))
    return data

def unique_disciplines(data):
    all_disciplines = set()
    for disciplines in data['disciplines']:
        all_disciplines.update(disciplines)
    return list(all_disciplines)

def binary_discipline_representation(data, discipline_list):
    discipline_matrix = np.zeros((len(data), len(discipline_list)), dtype=int)
    for i, disciplines in enumerate(data['disciplines']):
        for discipline in disciplines:
            discipline_matrix[i, discipline_list.index(discipline)] = 1
    return discipline_matrix

def initial_group_assignment(data, num_groups):
    np.random.seed(42)  # Fix the seed for reproducibility
    shuffled_indices = np.random.permutation(data.index)
    data['group'] = np.array([i % num_groups for i in range(len(data))])[shuffled_indices]
    return data

def optimize_groups(data, discipline_matrix, num_groups):
    changes = True
    while changes:
        changes = False
        # Calculate current diversity and group sizes
        current_diversity_score = calculate_diversity_score(data, discipline_matrix, num_groups)
        group_sizes = data['group'].value_counts().sort_index()

        for group1 in range(num_groups):
            for group2 in range(num_groups):
                if group1 != group2:
                    group1_data = data[data['group'] == group1]
                    group2_data = data[data['group'] == group2]

                    # Attempt swaps to improve diversity while maintaining group sizes
                    for idx1, idx2 in product(group1_data.index, group2_data.index):
                        # Swap
                        data.loc[idx1, 'group'], data.loc[idx2, 'group'] = data.loc[idx2, 'group'], data.loc[idx1, 'group']

                        # Evaluate changes
                        new_diversity_score = calculate_diversity_score(data, discipline_matrix, num_groups)
                        if new_diversity_score > current_diversity_score:
                            current_diversity_score = new_diversity_score
                            changes = True
                            break
                        else:
                            # Revert swap if no improvement in diversity
                            data.loc[idx1, 'group'], data.loc[idx2, 'group'] = data.loc[idx2, 'group'], data.loc[idx1, 'group']
                    if changes:
                        break
            if changes:
                break
    return data

def calculate_diversity_score(data, discipline_matrix, num_groups):
    score = 0
    for g in range(num_groups):
        group_data = data[data['group'] == g]
        # Calculate unique disciplines in the group
        unique_disciplines = np.unique(discipline_matrix[group_data.index], axis=0)
        score += np.sum(unique_disciplines)
    return score


def improved_diversity(discipline_matrix, data, num_groups):
    # Calculate diversity score for each group
    diversity_before = sum(np.unique(discipline_matrix[data['group'] == g], axis=0).sum() for g in range(num_groups))
    diversity_after = sum(np.unique(discipline_matrix[data['group'] == g], axis=0).sum() for g in range(num_groups))
    return diversity_after > diversity_before

def save_to_csv(data, output_file):
    data.to_csv(output_file, index=False)

# Example usage
file_path = 'data.csv'
output_file = 'grouped_students.csv'
num_groups = 6  # Set the desired number of groups

data = load_data(file_path)
discipline_list = unique_disciplines(data)
discipline_matrix = binary_discipline_representation(data, discipline_list)
data = initial_group_assignment(data, num_groups)
data = optimize_groups(data, discipline_matrix, num_groups)
save_to_csv(data, output_file)
