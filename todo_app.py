tasks=[]

def show_menu():
	print("\nTO DO LIST APP")
	print("\n1.VIEW TASKS")
	print("\n2.ADD TASK")
	print("\n3.MARK TASK AS COMPLETED")
	print("\n4.DELETE TASK")
	print("\n5.QUIT")


def view_tasks():
	if not tasks:
		print("No tasks available")

	else:
		for i,t in enumerate(tasks,1):
			status="Completed" if t["done"] else "Not Completed"
			print(f"{i}.{t['task']}-{status}")


def add_task():
	
	task=input("Enter task:").strip()
	if task:
		tasks.append({"task":task,"done":False})
		print("Task added successfully")
	else:
		print("Empty task not added")


def mark_done():
	view_tasks()
	try :
		num=int(input("Enter task number to mark done:"))
		if 1<=num<=len(tasks):
			tasks[num-1]["done"]=True
			print("Task marked as done\n")
		else:
			print("Invalid Task number")
	except ValueError:
		print("Enter valid number")
def delete_task():
	view_tasks()
	try:
		num=int(input("Enter task number to delete:"))
		if 1<=num<=len(tasks):
			removed=tasks.pop(num-1)
			print(f"Deleted task:{removed['task']}\n")
		else:
			print("Invalid Task number")
	except ValueError:
		print("Enter valid number")	
def main():
	while True:
		show_menu()
		try:
			choice=int(input("enter your choice:"))
		except ValueError:
			print("Enter valid number")	
		match choice:
			case 1:
				view_tasks()
			case 2:
				add_task()
			case 3:
				mark_done()
			case 4:
				delete_task()
			case 5:
				print("Good BYE")
				break
			case _:
				print("Invalid choice.Try again!")
if __name__=="__main__":
	main()
		
		
