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
      "resource"

For the code viewer during the eye tracking you can set the following document properties:

    code_viewer:
      status_bar_height: 40
      document:
        height_in_characters: 25
        font_pixel_size: 20
        margin_pixel_size: 0
        hide_scroll_bar: true
        padding_left: 0
        padding_top: 0
        padding_bottom: 0
        padding_right: 0
        use_leading_space: false
        tracking_devise: "eye tracker"
      side_bar_percentage_width: 0.2

Note: The `tracking_devise` option accepts "eye tracker" or "mouse". The system supports only the SMI RED-250 eye tracking devise.

### Resource directory

In the resource directory there is all the experimental material related to the experimental units, that is, the code in the versions needed to execute the experiment, the comprehension tasks and the general descriptions of the systems that will be presented to the subjects.

We adhere to the following structure:

    resource
    ├── paradigm1
    │   ├── system1
    │   │   ├── file1
    │   │   ├── ...
    │   │   ├── fileN
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

### System yaml file

Each experimental system has its own `.yaml` file to set the following properties:

    id:
      "id"
    name:
      "System1"
    enabled:
      True
    warmup:
      False
    description:
      "Small description"
    code:
      dci:
        resource/<paradigm1>/<system1>
      oo:
        resource/<paradigm2>/<system1>
    tasks:
      dci:
        [
          {
            id: "task1",
            name: "task1 name",
            description: "task 1 description",
            questions: ["question1", ..., "questionN"],
            options: ['--', 'true', 'false', 'dk']
          },
          ... ,
          {
            id: "taskN",
            ...
          }
        ]
      oo:
        [
          {
            id: "task1",
            ...
          },
          ...,
          {
            id: "taskN",
            ...
          }
        ]
