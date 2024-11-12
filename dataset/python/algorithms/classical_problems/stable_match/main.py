from functools import reduce


class StableMatch:
    def __init__(self, task_preferences_matrix, task_estimations_matrix):
        self.task_preferences_matrix = task_preferences_matrix
        self.task_estimations_matrix = task_estimations_matrix

    def get_stable_pairs_by_estimations(self):
        tasks = set(range(len(self.task_estimations_matrix)))
        pairs = dict([(user, None) for user in range(len(self.task_preferences_matrix))])
        while len(tasks) > 0:
            current_task = self.get_current_task(tasks)
            current_task_users_estimations = self.get_current_task_users_estimations(current_task)
            for estimation, user in current_task_users_estimations:
                task = pairs.get(user)
                if task is None:
                    pairs[user] = current_task
                    tasks.remove(current_task)
                    break
                else:
                    preference_for_task = self.task_preferences_matrix[user].index(task)
                    preference_for_current_task = self.task_preferences_matrix[user].index(current_task)
                    if preference_for_current_task < preference_for_task:
                        pairs[user] = current_task
                        tasks.remove(current_task)
                        tasks.add(task)
                        break
        return pairs

    def get_stable_pairs_by_preferences(self):
        tasks = set(range(len(self.task_estimations_matrix)))
        pairs = dict([(user, None) for user in range(len(self.task_preferences_matrix))])
        while len(tasks) > 0:
            current_task = self.get_current_task(tasks)
            current_task_users_priorities = self.get_current_task_users_priorities(current_task)
            for priority, user in current_task_users_priorities:
                task = pairs.get(user)
                if task is None:
                    pairs[user] = current_task
                    tasks.remove(current_task)
                    break
                else:
                    estimation_for_task = self.task_estimations_matrix[task][user]
                    estimation_for_current_task = self.task_estimations_matrix[current_task][user]
                    if estimation_for_current_task < estimation_for_task:
                        pairs[user] = current_task
                        tasks.remove(current_task)
                        tasks.add(task)
                        break
        return pairs

    def get_current_task_users_estimations(self, current_task):
        arr_size = len(self.task_estimations_matrix)
        users_estimations_array = [(self.task_estimations_matrix[current_task][i], i) for i in range(arr_size)]
        users_estimations_array.sort(key=lambda pair: pair[0])
        return users_estimations_array

    def get_current_task_users_priorities(self, current_task):
        arr_size = len(self.task_preferences_matrix)
        users_priorities_array = [(self.task_preferences_matrix[i].index(current_task), i) for i in range(arr_size)]
        users_priorities_array.sort(key=lambda pair: pair[0])
        return users_priorities_array

    def get_current_task(self, available_tasks):
        current_task = available_tasks.pop()
        available_tasks.add(current_task)
        return current_task

    def total_efficiency(self, pairs):
        matrix_elements = map(
            lambda item: self.task_estimations_matrix[item[1]][item[0]],
            pairs.items(),
        )
        return reduce(lambda acc, item: acc + item, matrix_elements)
