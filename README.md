# air_quality_acquisition

This is an app that pulls from EJScreen and Safecast API's for users to automatically acquire air quality data.
Air Quality and Environmental Justice: Combining Safecast and EPA EJScreen Data

Combining Safecast and EPA EJScreen data is a stand-alone script that allows users the ability to acquire/download air quality/radiation JSON data from Safecast and environmental/demographic JSON data from the Environmental Protection Agency's (EPA) Environmental Justice (EJ) Screen as a merged .csv based on location and date.

The program allows the user to enter coordinates for multiple specified locations, add a buffer from each location, and add a specified date range to acquire air quality, radiation levels, life expectancy, low income/minority areas, asthma/cancer/traffic levels, unemployment rates, among many more.

The script is compiled into four functions that perform as follows:

    1. Acquire EJScreen JSON formatted data from https://www.epa.gov/ejscreen and create a new data frame containing 
    environmental and demographic factors such as low income, minorites, cancer, life expectancy, air pollution, etc
    
    2. Acquire Safecast JSON formatted data from https://safecast.org/ and create a new data frame containing air 
    quality/radiation measurements such as units, values, time captured, and location, etc
    
    3. Merge both datasets as a single data frame based on the specified location
    
    4. Export the merged dataset as a .csv onto your local machine
    
Potential Users of this dataset include but are not limited to: local governments, academics, community organizations, and citizen scientists that have the ability to perform analysis to address environmental justice concerns such as determining susceptible populations within a proximity to radiation/bad air quality and exposure to environmental hazards.


Challenges and Limitations

The safecast data has its limitations due to the fact that it is entirely device dependent. If certain locations are lacking safecast devices, there is a lack of data collected within that specific area. In addition, if the device malfunctions then there are gaps in measurements over a range of time, which does not produce consistent measurements for some areas. The data is also limited in that locations of these readings are mapped to latitude-longitude values, which without a map requires more querying to determine where the location is in a human digestable way (city/state/country etc.). We were able to mitigate this issue by merging Safecast with EJSCreen data which did produce the city name associated with the coordinate values and have included that in the output.

The EPA EJScreen data has its limitations due to being a screening tool that cannot capture all of the relevant issues that should be considered such as all of the environmental concerns. Many of the environmental concerns are not yet included in comprehensive, nationwide databases such as drinking water quality and indoor air quality. It also relies on estimates that involve substantial uncertainty, especially true when using small geographic areas such as census block groups. Therefore, it is advisable to summarize data within a larger area that may cover several census block groups using a larger buffer. Lastly, the data is updated every 3-5 years so it may not be completely accurate.

The developers had some challenges in determining which U.S. cities had consistent recent Safecast data as a lot of the larger cities didn't have sufficient data to be used for output in the project. Users may be frustrated to not find data for certain cities across the US. Due to this project being completed for a master's level course and therefore having time limitations, there could have been more pre-processing and data cleaning to have created a more polished end product. Users can feel free to update the script as needed.


Download

The script is located on GitHub [here](https://github.com/MichaelAlgarra/air_quality_acquisition).


Using the Script

The extension of the script is .py so it can be accessed and run within any Python IDE


Contributors and Contact List

Mike Algarra - Master's of Science in Data Science (MSDS) Student at Drexel University, mja353@dragons.drexel.edu

Winn Costantini - Master's of Science in Data Science (MSDS) Student at Drexel University, wc555@drexel.edu

Shawn Oyer - Master's of Science in Data Science (MSDS) Student at Drexel University, sbo33@drexel.edu


License Use

Safecast Data: Data is published under a CC0 designation, meaning this is a public domain designation and the data is free and open for anyone to use under any circumstance. You are free to copy, edit and republish these, but you must make it clear Safecast is the original source and must publish under this same license. You can’t copyright anything you make based on Safecast's work. Source: https://safecast.org/about/licenses/

EPA EJScreen Data: Data is published to meet the intent of EO 12898, "Federal Actions to Address Enviornmental Justice in Minority Populations and Low-Income Populations." The data is released to the public to be more transparent about how the EPA considers environmental justice, and there is no mandate or guidance expressed that any entity should use its tool or its underlying data. Source: https://www.epa.gov/ejscreen/limitations-and-caveats-using-ejscreen

The script itself was developed by the three contributors as part of a group project during the Data Science Acquisition and Pre-Processing (DSCI 511) course at Drexel University. We place no restrictions on the script and can be used/modified freely.


Sources

United States Environmental Protection Agency. 2023 version. EJScreen. Retrieved: 10/19/2023, from www.epa.gov/ejscreen

Safecast.org. 2023 version. Retrieved: 10/19/2023, from https://safecast.org/
