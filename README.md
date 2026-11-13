# student-grades-pandas

Pandas exercise: merge five CSV files (student info, two quizzes, project, final exam), clean the data, compute a weighted final score and letter grade, and plot the grade distribution.

```bash
pip install -r requirements.txt
python grade_calculator.py
```

## Scoring (out of 20)
`(Quiz1 + Quiz2) × 0.25 + Project × 0.10 + Final × 0.25 + group bonus`, capped at 20.

- Quiz1 /10; Quiz2 is a letter mapped to points (A=10, B=8, C=6); Project /100; Final /20
- Missing quiz scores count as 0
- Group bonus: +1 if the group's average project score is above 80
- Grades: A > 18, B > 16, C > 14, D > 12, E otherwise

## Data
`data/` holds the sample CSV files (some quiz values are intentionally missing to practice cleaning). If these are real students' records, anonymise them before publishing.
