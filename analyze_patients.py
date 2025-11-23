import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

with open('patients_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
patients = data['patients']
plt.rcParams['font.family'] = 'DejaVu Sans'
fig = plt.figure(figsize=(20, 14))

# ========== ГРУППА 1: РАСПРЕДЕЛЕНИЕ ==========

# 1. Распределение по возрасту
ax1 = plt.subplot(3, 4, 1)
ages = [p['age'] for p in patients]
age_labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']
age_counts = [0] * len(age_labels)
for age in ages:
    if age < 30:
        age_counts[0] += 1
    elif age < 40:
        age_counts[1] += 1
    elif age < 50:
        age_counts[2] += 1
    elif age < 60:
        age_counts[3] += 1
    elif age < 70:
        age_counts[4] += 1
    else:
        age_counts[5] += 1
ax1.bar(age_labels, age_counts, color='steelblue', edgecolor='black')
ax1.set_xlabel('Возраст', fontsize=10)
ax1.set_ylabel('Кол-во', fontsize=10)
ax1.set_title('Распределение по возрасту', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
plt.setp(ax1.get_xticklabels(), fontsize=9)

# 2. Распределение по полу
ax2 = plt.subplot(3, 4, 2)
sex_counts = Counter([p['sex'] for p in patients])
sex_labels = {'male': 'М', 'female': 'Ж', 'other': 'Др.'}
labels = [sex_labels.get(k, k) for k in sex_counts.keys()]
sizes = list(sex_counts.values())
colors = ['#3498db', '#e74c3c', '#95a5a6']
ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(sizes)],
        textprops={'fontsize': 10})
ax2.set_title('Распределение по полу', fontsize=12, fontweight='bold')

# 3. Распределение по ИМТ
ax3 = plt.subplot(3, 4, 3)
bmi_categories = {'Недост.\nвес': 0, 'Норм.\nвес': 0, 'Избыт.\nвес': 0, 'Ожир.': 0}
for p in patients:
    height_m = p['height_cm'] / 100
    bmi = p['weight_kg'] / (height_m ** 2)
    if bmi < 18.5:
        bmi_categories['Недост.\nвес'] += 1
    elif bmi < 25:
        bmi_categories['Норм.\nвес'] += 1
    elif bmi < 30:
        bmi_categories['Избыт.\nвес'] += 1
    else:
        bmi_categories['Ожир.'] += 1
categories = list(bmi_categories.keys())
values = list(bmi_categories.values())
colors_bmi = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
ax3.bar(categories, values, color=colors_bmi, edgecolor='black')
ax3.set_ylabel('Кол-во', fontsize=10)
ax3.set_title('Распределение по ИМТ', fontsize=12, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
ax3.yaxis.set_major_locator(plt.MultipleLocator(2))
plt.setp(ax3.get_xticklabels(), fontsize=9)

# 4. Распределение по районам (круговая)
ax4 = plt.subplot(3, 4, 4)
districts = [p['address']['district'] for p in patients]
district_counts = Counter(districts)
district_labels_short = {
    'Индустриальный': 'Индустр.',
    'Ленинский': 'Ленинск.',
    'Свердловский': 'Свердл.',
    'Мотовилихинский': 'Мотовил.',
    'Дзержинский': 'Дзержин.',
    'Кировский': 'Кировск.',
    'Орджоникидзевский': 'Орджон.'
}
labels_dist = [district_labels_short.get(k, k) for k in district_counts.keys()]
sizes_dist = list(district_counts.values())
colors_dist = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
ax4.pie(sizes_dist, labels=labels_dist, autopct='%1.1f%%', startangle=90,
         colors=colors_dist[:len(sizes_dist)], textprops={'fontsize': 8})
ax4.set_title('Распределение по районам', fontsize=12, fontweight='bold')

# ========== ГРУППА 2: СРЕДНЕЕ ==========

# 5. Среднее кол-во болезней по возрасту
ax5 = plt.subplot(3, 4, 5)
age_disease_data = {label: [] for label in age_labels}
for p in patients:
    age = p['age']
    num_diseases = len(p['chronic_diseases'])
    if age < 30:
        age_disease_data['18-29'].append(num_diseases)
    elif age < 40:
        age_disease_data['30-39'].append(num_diseases)
    elif age < 50:
        age_disease_data['40-49'].append(num_diseases)
    elif age < 60:
        age_disease_data['50-59'].append(num_diseases)
    elif age < 70:
        age_disease_data['60-69'].append(num_diseases)
    else:
        age_disease_data['70+'].append(num_diseases)
avg_diseases_by_age = [np.mean(age_disease_data[label]) if age_disease_data[label] else 0
                       for label in age_labels]
ax5.plot(age_labels, avg_diseases_by_age, marker='o', linewidth=2.5,
         markersize=8, color='#9b59b6')
ax5.set_xlabel('Возраст', fontsize=10)
ax5.set_ylabel('Средн. кол-во', fontsize=10)
ax5.set_title('Среднее кол-во болезней по возрасту', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.yaxis.set_major_locator(plt.MultipleLocator(0.5))
ax5.yaxis.set_minor_locator(plt.MultipleLocator(0.25))
ax5.grid(which='minor', alpha=0.2)
plt.setp(ax5.get_xticklabels(), fontsize=9)

# 6. Среднее кол-во болезней по полу
ax6 = plt.subplot(3, 4, 6)
male_diseases = []
female_diseases = []
for p in patients:
    num_diseases = len(p['chronic_diseases'])
    if p['sex'] == 'male':
        male_diseases.append(num_diseases)
    elif p['sex'] == 'female':
        female_diseases.append(num_diseases)
avg_male = np.mean(male_diseases) if male_diseases else 0
avg_female = np.mean(female_diseases) if female_diseases else 0
ax6.bar(['Мужчины', 'Женщины'], [avg_male, avg_female],
        color=['#3498db', '#e74c3c'], edgecolor='black')
ax6.set_ylabel('Средн. кол-во', fontsize=10)
ax6.set_title('Среднее кол-во болезней по полу', fontsize=12, fontweight='bold')
ax6.grid(axis='y', alpha=0.3)
ax6.yaxis.set_major_locator(plt.MultipleLocator(0.5))
ax6.yaxis.set_minor_locator(plt.MultipleLocator(0.25))
ax6.grid(which='minor', alpha=0.2, axis='y')
plt.setp(ax6.get_xticklabels(), fontsize=9)

# 7. Среднее кол-во болезней по ИМТ
ax7 = plt.subplot(3, 4, 7)
bmi_disease_data = {cat: [] for cat in bmi_categories.keys()}
for p in patients:
    height_m = p['height_cm'] / 100
    bmi = p['weight_kg'] / (height_m ** 2)
    num_diseases = len(p['chronic_diseases'])
    if bmi < 18.5:
        bmi_disease_data['Недост.\nвес'].append(num_diseases)
    elif bmi < 25:
        bmi_disease_data['Норм.\nвес'].append(num_diseases)
    elif bmi < 30:
        bmi_disease_data['Избыт.\nвес'].append(num_diseases)
    else:
        bmi_disease_data['Ожир.'].append(num_diseases)
avg_diseases_by_bmi = [np.mean(bmi_disease_data[cat]) if bmi_disease_data[cat] else 0
                       for cat in bmi_categories.keys()]
ax7.bar(list(bmi_categories.keys()), avg_diseases_by_bmi,
        color=colors_bmi, edgecolor='black')
ax7.set_ylabel('Средн. кол-во', fontsize=10)
ax7.set_title('Среднее кол-во болезней по ИМТ', fontsize=12, fontweight='bold')
ax7.grid(axis='y', alpha=0.3)
ax7.yaxis.set_major_locator(plt.MultipleLocator(0.5))
ax7.yaxis.set_minor_locator(plt.MultipleLocator(0.25))
ax7.grid(which='minor', alpha=0.2, axis='y')
plt.setp(ax7.get_xticklabels(), fontsize=9)

# 8. Среднее кол-во болезней по районам
ax8 = plt.subplot(3, 4, 8)
district_disease_data = {d: [] for d in district_counts.keys()}
for p in patients:
    district = p['address']['district']
    num_diseases = len(p['chronic_diseases'])
    district_disease_data[district].append(num_diseases)
avg_diseases_by_district = {d: np.mean(district_disease_data[d]) if district_disease_data[d] else 0
                            for d in district_counts.keys()}
sorted_districts = sorted(avg_diseases_by_district.items(), key=lambda x: x[1], reverse=True)
district_names = [district_labels_short.get(d[0], d[0]) for d in sorted_districts]
district_avg_values = [d[1] for d in sorted_districts]
ax8.barh(district_names, district_avg_values, color=colors_dist[:len(district_names)], edgecolor='black')
ax8.set_xlabel('Средн. кол-во', fontsize=10)
ax8.set_title('Среднее кол-во болезней по районам', fontsize=12, fontweight='bold')
ax8.grid(axis='x', alpha=0.3)
ax8.xaxis.set_major_locator(plt.MultipleLocator(0.5))
ax8.xaxis.set_minor_locator(plt.MultipleLocator(0.25))
ax8.grid(which='minor', alpha=0.2, axis='x')
plt.setp(ax8.get_yticklabels(), fontsize=9)

# ========== ГРУППА 3: ОСТАЛЬНОЕ ==========

# 9. Топ-10 самых частых заболеваний
ax9 = plt.subplot(3, 4, 9)
all_diseases = []
for p in patients:
    all_diseases.extend(p['chronic_diseases'])
disease_counts = Counter(all_diseases)
top_diseases = disease_counts.most_common(10)
if top_diseases:
    diseases_names = [d[0] for d in top_diseases]
    diseases_values = [d[1] for d in top_diseases]
    short_names = []
    for name in diseases_names:
        if len(name) > 22:
            short_names.append(name[:19] + '...')
        else:
            short_names.append(name)
    ax9.barh(short_names, diseases_values, color='coral', edgecolor='black')
    ax9.set_xlabel('Кол-во', fontsize=10)
    ax9.set_title('10 самых частых заболеваний', fontsize=12, fontweight='bold')
    ax9.grid(axis='x', alpha=0.3)
    ax9.xaxis.set_major_locator(plt.MultipleLocator(2))
    plt.setp(ax9.get_yticklabels(), fontsize=8)

# 10. Тепловая карта: возраст и количество заболеваний
ax10 = plt.subplot(3, 4, 10)
disease_counts_matrix = [[0] * 7 for _ in range(6)]
for p in patients:
    age = p['age']
    num_diseases = min(len(p['chronic_diseases']), 6)
    if age < 30:
        age_idx = 0
    elif age < 40:
        age_idx = 1
    elif age < 50:
        age_idx = 2
    elif age < 60:
        age_idx = 3
    elif age < 70:
        age_idx = 4
    else:
        age_idx = 5
    disease_counts_matrix[age_idx][num_diseases] += 1
im = ax10.imshow(disease_counts_matrix, cmap='YlOrRd', aspect='auto')
ax10.set_xticks(range(7))
ax10.set_xticklabels(['0', '1', '2', '3', '4', '5', '6+'], fontsize=9)
ax10.set_yticks(range(6))
ax10.set_yticklabels(age_labels, fontsize=9)
ax10.set_xlabel('Кол-во болезней', fontsize=10)
ax10.set_ylabel('Возраст', fontsize=10)
ax10.set_title('Тепловая карта болезней', fontsize=12, fontweight='bold')
for i in range(6):
    for j in range(7):
        text = ax10.text(j, i, disease_counts_matrix[i][j],
                       ha="center", va="center", color="black", fontsize=8)
plt.colorbar(im, ax=ax10, fraction=0.046, pad=0.04)

# 11. Соотношение веса (расширенное)
ax11 = plt.subplot(3, 4, 11)
overweight_count = bmi_categories['Избыт.\nвес'] + bmi_categories['Ожир.']
underweight_count = bmi_categories['Недост.\nвес']
normal_count = bmi_categories['Норм.\nвес']
pie_labels = ['Норм.', 'Недост.', 'Лишний']
pie_values = [normal_count, underweight_count, overweight_count]
pie_colors = ['#2ecc71', '#3498db', '#e74c3c']
wedges, texts, autotexts = ax11.pie(pie_values, labels=pie_labels, autopct='%1.1f%%',
                                     startangle=90, colors=pie_colors, textprops={'fontsize': 10})
ax11.set_title('Категории веса', fontsize=12, fontweight='bold')

# 12. Сводная статистика
ax12 = plt.subplot(3, 4, 12)
ax12.axis('off')
underweight_key = 'Недост.\nвес'
normal_key = 'Норм.\nвес'
overweight_key = 'Избыт.\nвес'
obese_key = 'Ожир.'
underweight_val = bmi_categories[underweight_key]
normal_val = bmi_categories[normal_key]
overweight_val = bmi_categories[overweight_key]
obese_val = bmi_categories[obese_key]
stats_text = f"""СВОДНАЯ СТАТИСТИКА

Всего пациентов: {len(patients)}
Город: Пермь

По полу:
  Мужчин: {sex_counts.get('male', 0)} ({sex_counts.get('male', 0)/len(patients)*100:.1f}%)
  Женщин: {sex_counts.get('female', 0)} ({sex_counts.get('female', 0)/len(patients)*100:.1f}%)

По ИМТ:
  Недост. вес: {underweight_val} ({underweight_val/len(patients)*100:.1f}%)
  Норм. вес: {normal_val} ({normal_val/len(patients)*100:.1f}%)
  Избыт. вес: {overweight_val} ({overweight_val/len(patients)*100:.1f}%)
  Ожирение: {obese_val} ({obese_val/len(patients)*100:.1f}%)

Средн. болезней:
  Муж: {avg_male:.2f}
  Жен: {avg_female:.2f}
"""
ax12.text(0.05, 0.95, stats_text, transform=ax12.transAxes,
          fontsize=9, verticalalignment='top', family='monospace',
          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
fig.suptitle('Анализ базы данных пациентов поликлиники г. Пермь',
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()

print("\nАнализ завершен!")

plt.show()

