import glob
import os
import shutil

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
DEST_BASE_DIR = os.path.join("docs", "files")
BASE_TEMPLATE = """
# Talks and posters

Below are PDFs for talks and posters which have been given during GENESIS:

{links_rendered}

Please in get in touch on <l.c.denby@leeds.ac.uk>
"""


def copy_files(desc, dest_dir, source_glob):
    files = []

    print "Copying files from {}...".format(desc)

    START_DIR = os.path.curdir

    if not os.path.exists(os.path.join(DEST_BASE_DIR, dest_dir)):
        os.makedirs(os.path.join(DEST_BASE_DIR, dest_dir))

    source_dir = os.path.join(BASE_DIR, source_glob)

    source_parts = source_glob.split('/')
    name_pos = source_parts.index('*') - len(source_parts) - 1

    dirs = glob.glob(os.path.join(source_dir, "*.pdf"))
    for d in dirs:
        name = d.split('/')[name_pos]
        fn_new = os.path.join(DEST_BASE_DIR, dest_dir, "{}.pdf".format(name))
        print "\t{} \n\t -> {}".format(os.path.relpath(d), fn_new)
        shutil.copy(d, fn_new)
        files.append((name.replace("_", " "), fn_new.replace("docs/", "")))

    os.chdir(START_DIR)

    return files

def build_markdown(files):
    LINK_TEMPLATE = "- [{name}]({url})"
    links_rendered = "\n".join([LINK_TEMPLATE.format(name=name, url=url) for (name, url) in files])

    return BASE_TEMPLATE.format(links_rendered=links_rendered)

if __name__ == "__main__":
    files = []
    files += copy_files("posters at conferences", 'posters/', "conferences/*/poster")
    files += copy_files("posters for other trips", 'posters/', "trips/*/poster")
    files += copy_files("presentations at meetings", 'presentations/', "meetings/*/presentation")
    files += copy_files("presentations at conferences", 'presentations/', "conferences/*/presentation")
    files += copy_files("presentations generally", 'presentations/', "presentations/*")

    files = set(files)
    files = sorted(files, key=lambda f: f[0])

    print("Rendering template")
    with open(os.path.join("docs", "talks_and_posters.md"), "w") as fh:
        fh.write(build_markdown(files))
