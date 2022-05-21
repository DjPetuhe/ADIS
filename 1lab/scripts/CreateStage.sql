USE [footbal_Star]
GO

DROP TABLE #csv_temp
DROP TABLE #csv_temp_woom
DROP TABLE #csv_temp_world
GO

DROP TABLE [dbo].[intFootbalResults]
GO

DROP TABLE [dbo].[intFootbalResultsWoom]
GO

DROP TABLE [dbo].[WorldCupResults]
GO

/*========================================*
*		Table: IntFootbalResultsWoom
*=========================================*/

CREATE TABLE [dbo].[intFootbalResultsWoom](
	[date] [date] NOT NULL,
	[home_team] [nvarchar](50) NOT NULL,
	[away_team] [nvarchar](50) NOT NULL,
	[home_score] [int] NOT NULL,
	[away_score] [int] NOT NULL,
	[tournament] [nvarchar](50) NOT NULL,
	[city] [nvarchar](50) NOT NULL,
	[country] [nvarchar](50) NOT NULL,
	[neutral] [nvarchar](50) NOT NULL,
	[PK_intFootbalResults] int IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
) ON [PRIMARY]
GO

/*========================================*
*		Table: IntFootbalResults
*=========================================*/

CREATE TABLE [dbo].[intFootbalResults](
	[date] [date] NOT NULL,
	[home_team] [nvarchar](50) NOT NULL,
	[away_team] [nvarchar](50) NOT NULL,
	[home_score] [int] NOT NULL,
	[away_score] [int] NOT NULL,
	[tournament] [nvarchar](50) NOT NULL,
	[city] [nvarchar](50) NOT NULL,
	[country] [nvarchar](50) NOT NULL,
	[neutral] [nvarchar](50) NOT NULL,
	[PK_intFootbalResults] int IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
) ON [PRIMARY]
GO

/*========================================*
*		Table: WorldCupResults
*=========================================*/

CREATE TABLE [dbo].[WorldCupResults](
	[Year] [nvarchar](50) NOT NULL,
	[Datetime] [nvarchar](50) NOT NULL,
	[Stage] [nvarchar](50) NOT NULL,
	[Stadium] [nvarchar](50) NOT NULL,
	[City] [nvarchar](50) NOT NULL,
	[Home Team Name] [nvarchar](50) NOT NULL,
	[Home Team Goals] [int] NOT NULL,
	[Away Team Goals] [int] NOT NULL,
	[Away Team Name] [nvarchar](50) NOT NULL,
	[Win conditions] [nvarchar](50) NULL,
	[Attendence] [int] NULL,
	[Half-time Home Goals] [int] NOT NULL,
	[Half-time Away Goals] [int] NOT NULL,
	[Referee] [nvarchar](50) NOT NULL,
	[Assistant 1] [nvarchar](50) NOT NULL,
	[Assistant 2] [nvarchar](50) NOT NULL,
	[RoundID] [int] NOT NULL,
	[MatchID] [int] NOT NULL,
	[Home Team Initials] [nvarchar](50) NOT NULL,
	[Away Team Initials] [nvarchar](50) NOT NULL,
	[PK_WorldCupResults] int IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED
) ON [PRIMARY]
GO

/*========================================*
*		Upploading data to StageZones
*=========================================*/

CREATE TABLE #csv_temp(
	[date] [date] NOT NULL,
	[home_team] [nvarchar](50) NOT NULL,
	[away_team] [nvarchar](50) NOT NULL,
	[home_score] [int] NOT NULL,
	[away_score] [int] NOT NULL,
	[tournament] [nvarchar](50) NOT NULL,
	[city] [nvarchar](50) NOT NULL,
	[country] [nvarchar](50) NOT NULL,
	[neutral] [nvarchar](50) NOT NULL,
) ON [PRIMARY]
GO

BULK INSERT #csv_temp
FROM 'C:\Users\admin\Desktop\KPI\FourthSemestr\ADIS\1lab\datasets\sets\results.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '0x0a',
	CODEPAGE = '65001'
	);
GO

INSERT INTO [dbo].[intFootbalResults] ([date], home_team, away_team, home_score, away_score, tournament, city, country, neutral)
SELECT * FROM #csv_temp
GO

CREATE TABLE #csv_temp_woom(
	[date] [date] NOT NULL,
	[home_team] [nvarchar](50) NOT NULL,
	[away_team] [nvarchar](50) NOT NULL,
	[home_score] [int] NOT NULL,
	[away_score] [int] NOT NULL,
	[tournament] [nvarchar](50) NOT NULL,
	[city] [nvarchar](50) NOT NULL,
	[country] [nvarchar](50) NOT NULL,
	[neutral] [nvarchar](50) NOT NULL,
) ON [PRIMARY]
GO

BULK INSERT #csv_temp_woom
FROM 'C:\Users\admin\Desktop\KPI\FourthSemestr\ADIS\1lab\datasets\sets\woomresults.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '0x0a',
	CODEPAGE = '65001'
	);
GO

INSERT INTO [dbo].[intFootbalResultsWoom] ([date], home_team, away_team, home_score, away_score, tournament, city, country, neutral)
SELECT * FROM #csv_temp_woom
GO

CREATE TABLE #csv_temp_world(
	[Year] [nvarchar](50) NOT NULL,
	[Datetime] [nvarchar](50) NOT NULL,
	[Stage] [nvarchar](50) NOT NULL,
	[Stadium] [nvarchar](50) NOT NULL,
	[City] [nvarchar](50) NOT NULL,
	[Home Team Name] [nvarchar](50) NOT NULL,
	[Home Team Goals] [int] NOT NULL,
	[Away Team Goals] [int] NOT NULL,
	[Away Team Name] [nvarchar](50) NOT NULL,
	[Win conditions] [nvarchar](50) NULL,
	[Attendence] [int] NULL,
	[Half-time Home Goals] [int] NOT NULL,
	[Half-time Away Goals] [int] NOT NULL,
	[Referee] [nvarchar](50) NOT NULL,
	[Assistant 1] [nvarchar](50) NOT NULL,
	[Assistant 2] [nvarchar](50) NOT NULL,
	[RoundID] [int] NOT NULL,
	[MatchID] [int] NOT NULL,
	[Home Team Initials] [nvarchar](50) NOT NULL,
	[Away Team Initials] [nvarchar](50) NOT NULL,
) ON [PRIMARY]
GO

BULK INSERT #csv_temp_world
FROM 'C:\Users\admin\Desktop\KPI\FourthSemestr\ADIS\1lab\datasets\sets\WorldCupMatches.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ';',
	ROWTERMINATOR = '\n',
	CODEPAGE = '65001'
	);
GO

INSERT INTO [dbo].[WorldCupResults] (
	[Year],
	[Datetime],
	Stage,
	Stadium,
	City,
	[Home Team Name],
	[Home Team Goals],
	[Away Team Goals],
	[Away Team Name],
	[Win conditions],
	Attendence,
	[Half-time Home Goals],
	[Half-time Away Goals],
	Referee,
	[Assistant 1],
	[Assistant 2],
	RoundID,
	MatchID,
	[Home Team Initials],
	[Away Team Initials]
	)
SELECT * FROM #csv_temp_world
GO

SELECT * FROM [dbo].[WorldCupResults]
GO

SELECT * FROM [dbo].intFootbalResults
GO

SELECT * FROM [dbo].intFootbalResultsWoom
GO

ALTER TABLE Fact_Matches
ALTER COLUMN SecondAssistantID int NULL;