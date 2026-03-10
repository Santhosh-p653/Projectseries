
# Linear Programming Solver - Setup Instructions

This project is an interactive Python-based Linear Programming (LP) solver using **PuLP**.  
It supports **multiple variables and multiple constraints** and prints the optimal solution for your LP problem.

---

## 1. Clone the Repository

```bash
git clone <http://github.com/Santhosh-p653/projectSeries/LPPSolvery>
cd ProjectSeries/linear_programming_solver
2. Install Dependencies
Using requirements.txt

pip install -r requirements.txt
This will install:
PuLP (Python LP library)
Note: GLPK is required only if you want to use GLPK as a solver.
PuLP can also use its default CBC solver.
Installing GLPK (Optional / Recommended)
On Linux / Colab:

!apt-get install -y glpk-utils
On Windows:
Download GLPK binaries from: GLPK Windows�
Add the GLPK bin folder to your PATH environment variable.
PuLP will automatically detect GLPK if installed correctly.
If GLPK is not installed, PuLP will use the default CBC solver, which works on all platforms.
3. Run the LP Solver

python lp_solver.py
Enter the objective type: max or min
Enter number of variables
Enter coefficients for each variable in the objective function
Enter number of constraints
For each constraint, enter:
Coefficients of all variables
Sense (<=, >=, =)
RHS value
The program will then display:
Status: Optimal / Infeasible / Unbounded
Variable values: x1, x2, …
Optimal objective value: Z
4. Optional: Run in Google Colab
Open Colab: https://colab.research.google.com/�
Install dependencies:
Python

!pip install pulp
!apt-get install -y glpk-utils
Copy lp_solver.py code to a cell
Run interactive_lp_solver() and follow prompts
5. Project Structure

linear_programming_solver/
├── lp_solver.py        # Main interactive LP solver code
├── requirements.txt    # Python dependencies
├── setup.md            # Setup instructions (this file)
└── README.md           # Project overview and usage
6. Notes
Works for any number of variables and constraints
For 2-variable problems, you could optionally add graphical feasible region in the future
Supports both maximization and minimization problems


---

Broo, you can now **just save this as `setup.md`** in your repo, and it’s **ready for GitHub users** to follow.  

If you want, I can **also make a polished `README.md`** for this project so it looks **portfolio-ready and professional**.  

Do you want me to do that?
