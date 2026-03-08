from controller import CarnetAdressesController
from model import ContactModel

try:
    import ttkbootstrap

    from view2 import CarnetAdressesView
except ImportError:
    from view import CarnetAdressesView
    print("ttkbootstrap non installé, le view.py (tkinter classique) qui sera utilisé, pour une meilleure UI et une expérience esthétique installe ttkbootstrap (pip install ttkbootstrap)")

#from view import CarnetAdressesView

def main() -> None:
    model = ContactModel(db_path="contacts.db")
    view = CarnetAdressesView()
    CarnetAdressesController(model=model, view=view)
    view.root.mainloop()


if __name__ == "__main__":
    main()
