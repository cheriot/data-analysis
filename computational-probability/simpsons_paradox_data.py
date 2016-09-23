import numpy as np

prob_space = {
    ('female', 'A', 'admitted'): 0.019566946531153304,
    ('female', 'A', 'rejected'): 0.004295183384887301,
    ('female', 'B', 'admitted'): 0.0037560760053027007,
    ('female', 'B', 'rejected'): 0.0017675651789660005,
    ('female', 'C', 'admitted'): 0.044547061422890007,
    ('female', 'C', 'rejected'): 0.086473707467962915,
    ('female', 'D', 'admitted'): 0.028999116217410508,
    ('female', 'D', 'rejected'): 0.053855501546619514,
    ('female', 'E', 'admitted'): 0.020839593460008802,
    ('female', 'E', 'rejected'): 0.065992045956694709,
    ('female', 'F', 'admitted'): 0.0052739726027397011,
    ('female', 'F', 'rejected'): 0.070068493150684918,
    ('male', 'A', 'admitted'): 0.11301369863013702,
    ('male', 'A', 'rejected'): 0.069266460450729109,
    ('male', 'B', 'admitted'): 0.077949624392399511,
    ('male', 'B', 'rejected'): 0.045779938135218703,
    ('male', 'C', 'admitted'): 0.026568714096332307,
    ('male', 'C', 'rejected'): 0.045238621299160404,
    ('male', 'D', 'admitted'): 0.030404330534688506,
    ('male', 'D', 'rejected'): 0.061730004418912916,
    ('male', 'E', 'admitted'): 0.011816173221387503,
    ('male', 'E', 'rejected'): 0.030384445426425107,
    ('male', 'F', 'admitted'): 0.0049447635881573011,
    ('male', 'F', 'rejected'): 0.077467962881131211
}

gender_labels = ['female', 'male']  # axis 0
department_labels = ['A', 'B', 'C', 'D', 'E', 'F']  # axis 1
admission_labels = ['admitted', 'rejected']  # axis 2

gender_mapping = {label: index
                  for index, label in enumerate(gender_labels)}
department_mapping = {label: index
                      for index, label in enumerate(department_labels)}
admission_mapping = {label: index
                     for index, label in enumerate(admission_labels)}

joint_prob_table = np.zeros((2, 6, 2))

# read information from full probability space into the joint probability table
for gender, department, admission in prob_space:
    joint_prob_table[gender_mapping[gender],
                     department_mapping[department],
                     admission_mapping[admission]] = prob_space[(gender,
                                                                 department,
                                                                 admission)]

# Instructions given in problemset: https://courses.edx.org/courses/course-v1:MITx+6.008.1x+3T2016/courseware/1__Probability_and_Inference/joint_rv/
joint_prob_table[gender_mapping['female'], department_mapping['C'], admission_mapping['admitted']]
joint_prob_gender_admission = joint_prob_table.sum(axis=1)
joint_prob_gender_admission[gender_mapping['female'], admission_mapping['admitted']]

female_only = joint_prob_gender_admission[gender_mapping['female']]
prob_admission_given_female = female_only / np.sum(female_only)
prob_admission_given_female_dict = dict(zip(admission_labels, prob_admission_given_female))

print('Answer 1: %.3f' % prob_admission_given_female_dict['admitted'])

male_only = joint_prob_gender_admission[gender_mapping['male']]
prob_admission_given_male = male_only / np.sum(male_only)
prob_admission_given_male_dict = dict(zip(admission_labels, prob_admission_given_male))

print('Answer 2: %.3f' % prob_admission_given_male_dict['admitted'])

print('join_prob_gender_adminssion')
print(joint_prob_gender_admission)
admitted_only = joint_prob_gender_admission[:, admission_mapping['admitted']]
print(admitted_only)
prob_gender_given_admitted = admitted_only / np.sum(admitted_only)
prob_gender_given_admitted_dict = dict(zip(gender_labels, prob_gender_given_admitted))
print(prob_gender_given_admitted_dict)

from collections import defaultdict

joint_prob_dict = defaultdict(lambda: defaultdict(dict))
for gender, department, admission in prob_space:
    joint_prob_dict[department][gender][admission] = prob_space[(gender, department, admission)]
print(joint_prob_dict)

print(admission_labels)
for department in department_labels:
    for gender in gender_labels:
      gd_probs = joint_prob_table[gender_mapping[gender], department_mapping[department]]
      prob_admission = gd_probs[admission_mapping['admitted']] / np.sum(gd_probs)
      print('P(admission|%s,%s) = %.3f' % (department, gender[0], prob_admission))
