if __name__ == "__main__":
    if not __package__:
        # http://stackoverflow.com/questions/2943847/
        import sys, os
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        package_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, parent_dir)
        __import__(package_name)
        __package__ = package_name
        del sys, os

    from . import app
    from . import api, web # Initialize views
    app.run(debug=True)
