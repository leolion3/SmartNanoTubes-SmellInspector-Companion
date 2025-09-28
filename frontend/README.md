# SmellInspector Companion Frontend

This module contains the GUI of the SmellInspector companion.
It is ReactJS-based and uses TailwindCSS for pretty interfaces. 

## Installation

To run the frontend in production, please use the docker compose configuration under `software/`.
To run in development mode:

```bash
npm install
npm start
```

## Main Menu

After starting the software, you are presented with the dashboard overview:

![Dashboard image](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/home.png)

Here you can select between device management, substance management and test management.

## Add a new SmellInspector Device

To add a new SmellInspector device, click the device management card. You are then presented with the following view:

![Device management menu](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/available_devices_overview.png)

Here you can view previously-/connected devices and add new SmellInspector devices. To do so, click on the "New device" card, which then presents you with this interface:

![Add device interface](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/new_device.png)

The software will now perform a port scan to find connected SmellInspector devices. After devices are found, you will have the option of giving them a name and selecting the communication port.

> For MacOs/Linux - if multiple ports are present - please select the USB to UART serial port. This will ensure that the correct device driver is used.

> Note: If the USB to UART driver is not installed, the port scan will fail and you will be presented with an error message.

After the device is added, it will show up in the device overview.

## Reconnecting a SmellInspector device (Optional)

The software remembers previously connected SmellInspector devices using their Mac-Address. If you wish, you can reconnect previously connected devices by clicking on their card in the overview and then hitting the "Connect device" button in the device's details page:

![Reconnect device](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/disconnected_device.png)

> You can also just add the device using the usual "Add device" option. The software will delete the old device and replace it with the new one.

## Device management

After a device has been connected, it can be managed by clicking on its card in the device overview page. This will open a new page with the device details. Here, the fan speeds can be adjusted and the device can be disconnected before being ejected.

![Connected device details](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/device_overview.png)

> **Always use the disconnect button before unplugging the device to prevent test-data loss!** The device will not allow you to disconnect if it is currently in use!

## Substance management

Before starting a test, lets create some substances that are going to be measured. To do this, head to the "Substances" tab. Here you can view existing substances. "Air" is present by default and **cannot be removed**.

![Substances overview page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/substances.png)

> When starting a new test, the first substance is always set to "air". Ensure that no odors are present and allow the device at least 30 minutes to get adjusted before starting a measurement.

To add a new substance, simply click on the "Add new substance" card and then enter a substance name and, optionally, a quantity (50 muL, for instance).

![New substance page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/new_substance.png)

## Test management

To gather data from the SmellInspector and perform gas classification, head to the "Test management" page. Running tests will be displayed here.

> A "Test" refers to a test instance in which a SmellInspector device is being used. Data acquisition can be toggled on or off as desired. The "Test" is merely an abstraction layer to get live data from the sensor, display it, and perform classification.

![Test management page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/test_overview_empty.png)

To start a new test, click on "Start new test", then give the test a name and select the SmellInspector device to use. If you wish for the SmellInspector to be saved for later use, leave the "Save test-data" checkbox ticked. Unticking this checkbox can be used if you wish to only perform inference without adding new data to your existing dataset.

![New test page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/new_test.png)

After the test has been started, it will show up in the interface:

![New test page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/test_overview.png)

## Test and ML-Inference

To view data acquired from the SmellInspector, click the card for the test you just started. You will be presented with the following page:

![Running test page](https://raw.githubusercontent.com/leolion3/SmartNanoTubes-SmellInspector-Companion/refs/heads/main/frontend/_html/test_data.png)

The interface is split up into four section:

1. The top-left section displays the SmellInspector device's properties
	- The "ML-Classified Substance" string displays the output of the various classifiers from the enabled ML backends for the current data acquired from the SmellInspector.
	- The text-box under the device card displays the raw sensor data read from the SmellInspector.
2. The top-right section allows changing the substance that is currently being recorded.
	- This section is used for labelling test data and can be ignored if running in inference-only mode.
3. The bottom-left section displays the sensor data across the 64 sensor-channels rendered as a graph. The graph is limited to the last 100 recorded samples (~200 seconds).
4. The bottom-right section displays the averaged channel data across 4 sensors for each of the 16 channels per sensor as done by SmartNanoTubes.
	- To compute these values, channels `[i, i+16, i+32, i+48]` are summed and divided by 4 for each of the 16 channels of the smell.iX16 chip.

To stop a test, you can use the "Stop test" button.

> Note: When changing substances, the button will automatically use the last selected substance as the next available option, allowing one-click rotation between two substances without using the drop-down menu.
