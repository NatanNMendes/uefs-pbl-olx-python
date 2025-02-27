class View:
    @staticmethod
    def display_message(message: str):
        print(message)
    
    @staticmethod
    def display_menu(title: str, options: dict):
        print(f"\n=== {title} ===")
        for key, value in options.items():
            print(f"{key}. {value}")

    
    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt)
    
    @staticmethod
    def pause():
        input("Pressione Enter para continuar...")