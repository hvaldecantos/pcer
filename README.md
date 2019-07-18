# Program Comprehension Experiment Runner

A desktop application to gather data on the reading of source code by tracking the reader's gaze, file switching and use of scroll in large files.

## Configuration

### Configuration file

You need to add a `config.yml` to set general parameters to run the system.  
It needs the desired size for all the windows in the system:

    window_size:
      width: 1200
      height: 800

The path of the experimental resource to run the experiment:

    resource:
      "resource/"

### Resource directory

In the resource directory there is all the experimental material related to the experimental units, that is, the code in the versions needed to execute the experiment, the comprehension tasks and the general descriptions of the systems that will be presented to the subjects.

We adhere to the following structure:

# Program Comprehension Experiment Runner

A desktop application to gather data on the reading of source code by tracking the reader's gaze, file switching and use of scroll in large files.

## Configuration

### Configuration file

You need to add a `config.yml` to set the general parameters to run the system.  
It needs the desired size for all the windows in the system:

    window_size:
      width: 1200
      height: 800

The path of the experimental resource to run the experiment:

    resource:
      "resource/"

### Resource directory

In the resource directory there is all the experimental material related to the experimental units, that is, the code in the versions needed to execute the experiment, the comprehension tasks and the general descriptions of the systems that will be presented to the subjects.

We adhere to the following structure:

    resource
    ├── paradigm1
    │   ├── system1
    │   │   ├── code
    │   │   │   ├── file1
    │   │   │   ├── ...
    │   │   │   └── fileN
    │   │   └── tasks
    │   │       ├── task1
    │   │       ├── ...
    │   │       └── taskN
    │   ├── system2
    │   ├── ...
    │   └── systemN
    ├── paradigm2
    │   ├── system1
    │   ├── ...
    │   └── systemN
    ├── system1.yml
    ├── ...
    └── systemN.yml
