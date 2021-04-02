#Henry Underhill - Inside Edge Python Hiring Test
import pandas as pd
import numpy as np

#INSTRUCTIONS (copied from original repo)

    #Create a GitLab account (if you don't already have one).
    #Clone this repository to your machine.
    #Install it using pip install -r requirements.txt

    #Modify run.py to perform the following steps when called via python run.py:

    #Read in ./data/raw/pitchdata.csv

    #Perform grouping/aggregations of each combination from
    #./data/reference/combinations.txt to create tables/dataframes.
    #Round the stat to a max of three decimal places.
    #Only include subjects with PA >= 25.
    #Combine each individual table/dataframe into a single one with the
    #following column headers:
        
        #SubjectId (e.g. 108, 119, etc)
        #Stat (e.g. the name of the stat "AVG", "OBP", etc.)
        
        #Split (e.g. "vs LHP", "vs RHH", etc.)

    #Subject (e.g. "HitterId", "PitcherTeamId", etc.)
    
    #Value (e.g. the value of the Stat 0.350, 1.03, 0.5, etc)

    #Sort the table/dataframe on the first four columns (each in ascending order).
    #Save the csv to ./data/processed/output.csv

    #Run the test suite by opening a command-line, cd in to the repo, and running
    #the following command: pytest -v

    #Upload to a new repository under your own GitLab/GitHub/BitBucket account.

#-----------------------------------------------------------------------------#
#Begin work#

#MY APPROACH

    #My plan is to start by reading in the data, and then create 4 separate
    #dataframes. The four dataframes will be for each type of subject:
        #Individual hitter, individual pitcher, team hitter, and team pitcher.
    #I will do this all using pandas, and the groupby function will be our
    #best friend for narrowing these down with ease. I will also use the sum
    #function to easily add all separate plat appearances together.
    #These 4 dataframes will all use the same code shell.
def main():
    
    #read in the raw data
    df = pd.read_csv("./data/raw/pitchdata.csv")
    df.head()
    
    #---------------------------------------------------------------#
    
    #INDIVIDUAL HITTERS#
    
    #grouping function to narrow down to just individual hitters
    #using sum() to add all plate appearances together
    #I am also adding H, TB, BB, etc for later use when we calculate BA,
    #OBP, SLG, and OPS.
    indv_hitter = df.groupby(['HitterId', 'PitcherSide'], 
                             as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()

    #subsetting based on 25 or more plate appearances
    indv_hitter = indv_hitter[indv_hitter.PA >= 25]
    
    #renaming HitterId to SubjectId for the final dataframe
    indv_hitter.rename(columns = {'HitterId':'SubjectId'},inplace = True)
    
    #using loc statements to change the PitcherSide variable into splits 
    indv_hitter.loc[indv_hitter['PitcherSide'] == 'L', 'Split'] = 'vs LHP' 
    indv_hitter.loc[indv_hitter['PitcherSide'] == 'R', 'Split'] = 'vs RHP' 
    
    #creating a subject variable that will be the same for all rows grouped
    indv_hitter['Subject'] = 'HitterId'
    
    indv_hitter.head()
    
     #---------------------------------------------------------------#
    
    #INDIVIDUAL PITCHERS#

    #same grouping technique as earlier, but this time using PitcherID
    indv_pitcher = df.groupby(['PitcherId','HitterSide'], 
                              as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    
    #subsetting based on 25 or more plate appearances
    indv_pitcher = indv_pitcher[indv_pitcher.PA >= 25]
    
    #renaming PitcherID to SubjectId for the final dataframe
    indv_pitcher.rename(columns = {'PitcherID':'SubjectId'},inplace = True)
    
    #using loc statements to change the HitterSide variable into splits 
    indv_pitcher.loc[indv_pitcher['HitterSide'] == 'L', 'Split'] = 'vs LHH' 
    indv_pitcher.loc[indv_pitcher['HitterSide'] == 'R', 'Split'] = 'vs RHH' 
    
    #creating a subject variable that will be the same for all rows grouped
    indv_pitcher['Subject'] = 'PitcherId'
    
    indv_pitcher.head()
    
#---------------------------------------------------------------#
    
    #TEAM HITTERS#
    
    #Now we will move to team hitters. The approach I am taking for teams vs
    #individuals is basically identical. We are keeping individual pitchers
    #for the grouping, as we still need to split between right handed
    #and left handed pitchers. The same will go for when we do team pitchers.
    team_hitter = df.groupby(['HitterTeamId','PitcherSide'], 
                             as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    
    #subsetting based on 25 or more plate appearances
    team_hitter = team_hitter[team_hitter.PA >= 25]
    
    #renaming HitterId to SubjectId for the final dataframe
    team_hitter.rename(columns = {'HitterTeamId':'SubjectId'},inplace = True)
    
    #using loc statements to change the PitcherSide variable into splits 
    team_hitter.loc[team_hitter['PitcherSide'] == 'L', 'Split'] = 'vs LHP' 
    team_hitter.loc[team_hitter['PitcherSide'] == 'R', 'Split'] = 'vs RHP' 
    
    #creating a subject variable that will be the same for all rows grouped
    team_hitter['Subject'] = 'HitterTeamId'
    
     #---------------------------------------------------------------#
    
    #TEAM PITCHERS#

    #same grouping technique as earlier, but this time using PitcherTeamID
    #using individual hitters still in order to differentiate between left
    #handed vs right handed hitters
    team_pitcher = df.groupby(['PitcherTeamId','HitterSide'], 
                              as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    
    #subsetting based on 25 or more plate appearances
    team_pitcher = team_pitcher[team_pitcher.PA >= 25]
    
    #renaming PitcherID to SubjectId for the final dataframe
    team_pitcher.rename(columns = {'PitcherTeamID':'SubjectId'},inplace = True)
    
    #using loc statements to change the HitterSide variable into splits 
    team_pitcher.loc[team_pitcher['HitterSide'] == 'L', 'Split'] = 'vs LHH' 
    team_pitcher.loc[team_pitcher['HitterSide'] == 'R', 'Split'] = 'vs RHH' 
    
    #creating a subject variable that will be the same for all rows grouped
    team_pitcher['Subject'] = 'PitcherTeamId'
    
    #---------------------------------------------------------------#
    
    #Now that we have constructed dataframes for each of the four subject
    #groups, we are now ready to combine the four into one large dataframe.
    #We will do this using the concat() function
    
    frames = [indv_hitter, indv_pitcher, team_hitter, team_pitcher]
    output = pd.concat(frames)
    
    #Now we must create values for each of our four statistics we wish to
    #calculate, those being AVG, OBP, SLG, and OPS. We will now add these
    #values to our final dataframe, titled 'output'. We will round to three
    #decimals using the basic python function, round(3).
    
    #The calculations are simple, and are as follows:
        #BA = H / AB
        #OBP = H + BB + HBP / PA
        #SLG = TB / AB
        #OPS = OBP + SLG
        
    #BA calculation first
    output['AVG'] = (output.H / output.AB).round(3)
    output['OBP'] = ((output.H + output.BB + output.HBP) / output.PA).round(3)
    output['SLG'] = (output.TB / output.AB).round(3)
    output['OPS'] = (output.OBP + output.SLG).round(3)
    
    #Next we need to pivot the dataset. We need to do this so we can create a
    #variable for Stat. The Stat will check if the number associated with
    #this particular player or team is 1 of 4 categories we used before: AVG, 
    #OBP, SLG, and OPS.
    
    output.head()
    
    #Now we can remove the variables for Pitcher Side and Hitter Side, since
    #we effectively replaced those both with the Split variable
    output.drop(['PitcherSide', 'HitterSide'], axis = 1)
    
    #Time to pivot long!
    output = pd.melt(output, id_vars = ['SubjectId','Split','Subject'], 
                             value_vars = ['AVG','OBP','OPS','SLG'],
                             var_name = 'Stat', value_name = 'Value')
    
    #Lastly, we sort 
    output = output.sort_values(by = ['SubjectId','Stat','Split','Subject'])
    output = output['SubjectId','Stat','Split','Subject','Value']
    output.to_csv('./data/processed/output.csv',index = False)
    
    pass


if __name__ == '__main__':
    main()
