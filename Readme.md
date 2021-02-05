## Known Issues

Automated builds are NOT functional. See [azure/functions-action#52](/azure/functions-action/issues/52) for details, but once that works, it should be fine.
In the meantime, use Visual Studio Code, make sure Docker is installed (on Windows or Linux) and the "Build cncli" task.

## Installation

1. Use the Visual Studio Code "Build cncli" task to build the cncli executable. This requires git and docker installed. The script can be run separately (*This will take a while, you can move on to step 2 before it completes, but make sure it is finished before trying step 3.*):  

    `git clone https://github.com/AndrewWestberg/cncli.git`

    `docker run -v ./cncli:/volume --rm -t clux/muslrust cargo build --release`

    `mv ./cncli/target/x86_64-unknown-linux-musl/release/cncli ./functions/bin`

2. The azuredeploy.json in the templates directory will set up the Azure infrastructure for the function app. This file isn't fully parameterized, so if you need different scaling, it may need tweaking. There are only two parameters:

    * base_name - the name that will be used for the beginning of each resource
    created.
    * telegram_bot_token - The bot token that the function uses to let you know when
    there's an issue. This can be left blank then updated in the Function App
    Configuration after deployment, but just know that it will cause issues.

3. Once the infrastructure is in place, use either Visual Studio Code or the [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools) to deploy the function:

   `func azure publish <base_name>functionappsvc`

## Configuration

The system uses a combination of Function App configuration settings and a file in blob storage for the majority of it's configuration. The most significant portion is the ping.config file in the function-config container in the storage account created by the ARM template. The format is straightforward, and the sample data is obvious. 

The only thing worth noting is that the telegramRecipients is a string, and can contain more than one recipient, separated by a comma. It has NOT been tested with spaces in the string.

Currently, it pings every server in the list every 5 minutes. To change the timing, modify the functions/CronPing/function.json trigger schedule.