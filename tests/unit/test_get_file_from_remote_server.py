import os
from actions import get_file_from_remote_server as get
from pathlib import Path


def test_no_file(sftp, capsys):
    """Test what happens when you ask to transfer a
    file which doesn't exist.
    """

    assert get.get(sftp, "totes.not.fake.no.really") is False
    assert get.FILE_NOT_FOUND_ERROR_MESSAGE in capsys.readouterr().out


def test_best_case(sftp):
    """This tests what happens if you get a file that does exist on
    the remote server
    """

    # Create file locally
    f = open('test.txt', 'w')
    f.write('testing')
    f.close()

    # Put file on the remote server
    sftp.put('test.txt', 'test.txt', preserve_mtime=False)

    # Test getting file
    assert get.get(sftp, "test.txt") is True

    # Remove local file
    os.remove('test.txt')

    # Remove remote file
    sftp.remove('test.txt')


def test_local_dir_case(sftp, capsys):
    """This tests what happens if you get a file that already exists
    as a directory locally
    """


    # Create file locally
    filename = 'test_local_dir_case'
    f = open(filename, 'w')
    f.write('testing')
    f.close()

    # Put file on the remote server
    sftp.put(filename, filename, preserve_mtime=False)

    # Remove local files
    os.remove(filename)

    # Create directory locally
    if not os.path.exists(filename):
        os.makedirs(filename)

    # Test getting file
    assert get.get(sftp, filename) is False
    assert get.IS_DIRECTORY_ERROR in capsys.readouterr().out

    # Remove local directory
    os.removedirs(filename)

    # Remove remote files
    sftp.remove(filename)


def test_remote_dir_case(sftp, capsys):
    """This tests what happens if you try to get a directory that exists
    on the remote server
    """

    # Add directory to the remote server
    foldername = 'test_remote_dir_case'
    sftp.mkdir(foldername)

    # Test getting directory with get()
    assert get.get(sftp, foldername) is False
    assert get.IO_ERROR_MESSAGE in capsys.readouterr().out

    # Remove remote directory
    sftp.rmdir(foldername)

    # Remove local file
    os.remove(foldername)


def test_no_permissions_case(sftp, capsys):
    """This tests what happens if you get a file that you don't have permissions
    to write
    """

    # Create file locally
    filename = 'test_no_permissions_case'
    f = open(filename, 'w')
    f.write('testing')
    f.close()

    # Save directory path
    path = Path().absolute()

    # Put file on the remote server
    sftp.put(filename, filename, preserve_mtime=False)

    # Change current directory path
    os.chdir('/')

    # Test getting file
    assert get.get(sftp, "filename") is False
    assert get.PERMISSION_ERROR_MESSAGE in capsys.readouterr().out

    # Change back to most recent directory
    os.chdir(path)

    # Remove local files
    os.remove(filename)

    # Remove remote files
    sftp.remove(filename)

