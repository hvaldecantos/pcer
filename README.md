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
      sidebar:
        percentage_width: 0.2
        font_pixel_size: 18
        font_type: "Courier"

Note: The code viewer is a window that shows a sidebar and a document area. At the left is the sidebar with a list of files from the current experimental system, and at the wight is the document area with the source code for the participant to read.

For the tracking device use the following properties:

    tracker:
      device: "eye tracker"
      tracking_data_path: "tracking_data"

Note: The `device` option accepts "eye tracker" or "mouse". The system supports only the SMI RED-250 eye tracking device.

For specific eye tracker configuration:

    tracker:
      eye_tracker:
        calibration_points: 5
        calibration_accuracy_limit: 1.0
        network:
          send_ip: '192.168.74.1'
          send_port: 4444
          receive_ip: '192.168.74.2'
          receive_port: 5555
        draw_gaze: true

For the form windows use the following properties:

    form:
      font:
        type: "Arial"
        title_size: 25
        title_bold: true
        description_size: 22
      end:
        title: "The experiment has finished."
        message: "There are no more experimental systems. \nThank you for your time."

For the time limit for each experimental system:

    time_limit:
      minutes: 15
      seconds: 0

For highlighting the keyword in different language used

    keywords:
      common: ["abstract", "continue", "for", "new", "switch", "assert", "default", "goto", "package",
               "synchronized", "boolean", "do", "if", "private", "this", "break", "double", "implements",
               "protected", "throw", "byte", "else", "import", "public", "throws", "case", "enum",
               "intanceof", "return", "transient", "catch", "extends", "int", "short", "try", "char",
               "final", "interface", "static", "void", "class", "finally", "long", "strictfp", "volatile",
               "const", "float", "native", "super", "while", "true", "false", "null"]
      oo_bold: ["class", "interface"]
      oo_italic: ["abstract"]
      dci_bold: ["class", "interface", "context", "role", "stageprop", "requires"]
      dci_italic: ["requires"]


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
