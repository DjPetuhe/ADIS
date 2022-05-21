using System;
using System.Linq;
using System.Collections.Generic;

namespace Adis_FirstLab
{
    static class ETL
    {
        //Filling Date Table
        public static void FillDateTable(footbal_StarEntities context)
        {
            var allDatesInt = context.intFootbalResults.Select(d => d.date)
                                                       .Union(context.intFootbalResultsWoom
                                                                     .Select(d => d.date));
            var worldCupDates = context.WorldCupResults.Select(d => d.Datetime)
                                                       .Distinct()
                                                       .AsEnumerable()
                                                       .Select(d => new DateTime (StrToDateTime(d).Item1, StrToDateTime(d).Item2, StrToDateTime(d).Item3));
            var allDates = allDatesInt.Union(worldCupDates).ToList();
            allDates.Sort();
            foreach(var date in allDates)
            {
                Date current = new Date() { Year = date.Year, Month = date.Month, Day = date.Day };
                context.Date.Add(current);
            }
        }
        
        //Filling Referee Table
        public static void FillRefereeTable(footbal_StarEntities context)
        {
            var allReferies = from matches in context.WorldCupResults
                              select matches.Referee;
            allReferies = allReferies.AsQueryable().Distinct();
            foreach (string referee in allReferies)
            {
                Referee current = new Referee() { RefereeName = referee };
                context.Referee.Add(current);
            }
        }

        //Filling Assistant Table
        public static void FillAssistantTable(footbal_StarEntities context)
        {
            var allAssistants = context.WorldCupResults.Select(a => a.Assistant_1)
                                                       .Union(context.WorldCupResults
                                                                     .Select(a => a.Assistant_2));
            foreach (var assist in allAssistants)
            {
                Assistant current = new Assistant() { AssitantName = assist };
                context.Assistant.Add(current);
            }
        }

        //Filling Tournament Table
        public static void FillTournamentTable(footbal_StarEntities context)
        {
            var allTournaments = context.intFootbalResults.Select(t => t.tournament)
                                                          .Union(context.intFootbalResultsWoom
                                                                        .Select(t => t.tournament))
                                                          .AsQueryable()
                                                          .Distinct();
            foreach (var tourn in allTournaments)
            {
                Tournament current = new Tournament() { TournamentName = tourn };
                context.Tournament.Add(current);
            }
        }

        //Filling Team Table
        public static void FillTeamTable(footbal_StarEntities context)
        {
            var allTeamsMens = context.intFootbalResults
                                  .Select(t => t.home_team)
                                  .Union(context.intFootbalResults
                                                .Select(t => t.away_team));
            var allTeamsWooms = context.intFootbalResultsWoom
                                  .Select(t => t.home_team)
                                  .Union(context.intFootbalResultsWoom
                                                .Select(t => t.away_team));
            var allTeamsWorldCup = context.WorldCupResults
                                  .Select(t => t.Home_Team_Name)
                                  .Union(context.WorldCupResults
                                                .Select(t => t.Away_Team_Name));
            var allTeams = allTeamsMens.Union(allTeamsWooms).Union(allTeamsWorldCup).ToList();
            for (int i = 0; i < allTeams.Count; i++)
            {
                allTeams[i] = ClearName(allTeams[i]);
            }
            allTeams = allTeams.AsQueryable().Distinct().ToList();
            foreach (var team in allTeams)
            {
                Team current = new Team() { TeamName = team };
                context.Team.Add(current);
            }
        }

        //Filling Location Table
        public static void FillLocationTable(footbal_StarEntities context)
        {
            var locationsMen = context.intFootbalResults.Select(l => new { country = l.country, city = l.city })
                                                        .Distinct()
                                                        .AsEnumerable()
                                                        .Select(l => new Loc { Country = l.country, City = l.city });
            var locationsWoom = context.intFootbalResultsWoom.Select(l => new { country = l.country, city = l.city })
                                                         .Distinct()
                                                         .AsEnumerable()
                                                         .Select(l => new Loc { Country = l.country, City = l.city });
            var locationsWorld = context.WorldCupResults.Select(l => new { year = l.Year, city = l.City, stadium = l.Stadium })
                                                        .Distinct()
                                                        .AsEnumerable()
                                                        .Select(l => new Loc { Country = getWorldCupHost(Convert.ToInt32(l.year), l.city), City = l.city, Stadium = l.stadium });
            var allLocations = locationsMen.Union(locationsWoom).Union(locationsWorld);
            foreach (var location in allLocations)
            {
                Location current = new Location() { CountryName = location.Country, City = location.City, Stadium = location.Stadium };
                context.Location.Add(current);
            }
        }

        //Filling Fact Table
        public static void FillFactTable(footbal_StarEntities context)
        {
            var matchMen = context.intFootbalResults.Select(m => m)
                                                    .AsEnumerable()
                                                    .Select(m => new Fact
                                                    {
                                                        Date = m.date,
                                                        HomeTeam = ClearName(m.home_team),
                                                        AwayTeam = ClearName(m.away_team),
                                                        HomeScore = m.home_score,
                                                        AwayScore = m.away_score,
                                                        Tourn = m.tournament,
                                                        City = m.city,
                                                        Country = m.country,
                                                        Wooms = false
                                                    });
            var matchWooms = context.intFootbalResultsWoom.Select(m => m)
                                                          .AsEnumerable()
                                                          .Select(m => new Fact
                                                          {
                                                              Date = m.date,
                                                              HomeTeam = ClearName(m.home_team),
                                                              AwayTeam = ClearName(m.away_team),
                                                              HomeScore = m.home_score,
                                                              AwayScore = m.away_score,
                                                              Tourn = m.tournament,
                                                              City = m.city,
                                                              Country = m.country,
                                                              Wooms = true
                                                          });
            var matchWorldCup = context.WorldCupResults.Select(m => m)
                                                       .AsEnumerable()
                                                       .Select(m => new Fact
                                                       {
                                                           Date = new DateTime(StrToDateTime(m.Datetime).Item1, StrToDateTime(m.Datetime).Item2, StrToDateTime(m.Datetime).Item3),
                                                           HomeTeam = ClearName(m.Home_Team_Name),
                                                           AwayTeam = ClearName(m.Away_Team_Name),
                                                           HomeScore = m.Home_Team_Goals,
                                                           AwayScore = m.Away_Team_Goals,
                                                           Tourn = "FIFA World Cup",
                                                           City = m.City,
                                                           Country = getWorldCupHost(Convert.ToInt32(m.Year), m.City),
                                                           Stadium = m.Stadium,
                                                           Wooms = false,
                                                           Assistant1 = m.Assistant_1,
                                                           Assistant2 = m.Assistant_2,
                                                           Referee = m.Referee
                                                       });
            var allMatches = matchMen.Union(matchWooms).Union(matchWorldCup).Distinct().ToList();
            List<Fact_Matches> matchs = new List<Fact_Matches>();
            int i = 0;
            foreach (var match in allMatches)
            {
                i++;
                match.FindIDs(context);
                Fact_Matches current = new Fact_Matches {
                                                            FirstTeamID = match.HomeTeamID,
                                                            SecondTeamID = match.AwayTeamID,
                                                            LocationID = match.LocID,
                                                            DateID = match.DateID,
                                                            RefereeID = match.RefereeID,
                                                            TournamentID = match.TournID,
                                                            FirstAssistantID = match.Assistant1ID,
                                                            SecondAssistantID = match.Assistant2ID,
                                                            FirstTeamScore = match.HomeScore,
                                                            SecondTeamScore = match.AwayScore,
                                                            neutral = match.neutral,
                                                            Woomans = match.Wooms
                                                        };
                matchs.Add(current);
                if (i % 100 == 0) Console.WriteLine(i);
            }
            context.Fact_Matches.AddRange(matchs);
        }

        //auxiliary struct to import facts to fact_table
        private struct Fact
        {
            public DateTime Date { get; set; }
            public int DateID { get; private set; }
            public string HomeTeam { get; set; }
            public int HomeTeamID { get; private set; }
            public string AwayTeam { get; set; }
            public int AwayTeamID { get; private set; }
            public int HomeScore { get; set; }
            public int AwayScore { get; set; }
            public string Tourn { get; set; }
            public int TournID { get; private set; }
            public string City { get; set; }
            public string Country { get; set; }
            public string Stadium { get; set; }
            public int LocID { get; private set; }
            public string Assistant1 { get; set; }
            public int? Assistant1ID { get; private set; }
            public string Assistant2 { get; set; }
            public int? Assistant2ID { get; private set; }
            public string Referee { get; set; }
            public int? RefereeID { get; private set; }
            public bool Wooms { get; set; }
            public bool neutral { get; set; }

            public void FindIDs(footbal_StarEntities context)
            {
                DateTime temp = Date;
                DateID = context.Date.Where(m => m.Year == temp.Year && m.Month == temp.Month && temp.Day == m.Day).Select(m => m.DateID).First();
                string tempStr = HomeTeam;
                HomeTeamID = context.Team.Where(m => m.TeamName == tempStr).Select(m => m.TeamID).First();
                tempStr = AwayTeam;
                AwayTeamID = context.Team.Where(m => m.TeamName == tempStr).Select(m => m.TeamID).First();
                tempStr = Tourn;
                TournID = context.Tournament.Where(m => m.TournamentName == tempStr).Select(m => m.TournamentID).First();
                string tempCountry = Country;
                string tempCity = City;
                string tempStadium = Stadium;
                LocID = context.Location.Where(m => m.CountryName == tempCountry && m.City == tempCity && m.Stadium == tempStadium).Select(m => m.LocationID).First();
                if (!string.IsNullOrEmpty(Assistant1))
                {
                    tempStr = Assistant1;
                    Assistant1ID = context.Assistant.Where(m => m.AssitantName == tempStr).Select(m => m.AssistantID).First();
                }
                if (!string.IsNullOrEmpty(Assistant2))
                {
                    tempStr = Assistant2;
                    Assistant2ID = context.Assistant.Where(m => m.AssitantName == tempStr).Select(m => m.AssistantID).First();
                }
                if (!string.IsNullOrEmpty(Referee))
                {
                    tempStr = Referee;
                    RefereeID = context.Referee.Where(m => m.RefereeName == tempStr).Select(m => m.RefereeID).First();
                }
                neutral = !(HomeTeam == Country || AwayTeam == Country);
            }
        }

        //Auxiliary struct to import locations to table
        private struct Loc
        {
            public string Country { get; set; }
            public string City { get; set; }
            public string Stadium { get; set; }
        }

        //Clearing names from trash
        private static string ClearName(string team)
        {
            team = team.Replace("\"rn\"", "");
            team = team.Replace("\"", "");
            return team.Replace(">", "");
        }

        //From str monthes to int
        private static int MonthToInt(string month)
        {
            switch (month)
            {
                case "Jan":
                case "January": return 1;
                case "Feb":
                case "February": return 2;
                case "Mar":
                case "March": return 3;
                case "Apr":
                case "April": return 4;
                case "May": return 5;
                case "Jun":
                case "June": return 6;
                case "Jul":
                case "July": return 7;
                case "Aug":
                case "August": return 8;
                case "Sep":
                case "Sept":
                case "September": return 9;
                case "Oct":
                case "October": return 10;
                case "Nov":
                case "November": return 11;
                case "Dec":
                case "December": return 12;
                default: return 0;
            }
        }

        //Info about world cup countries
        private static string getWorldCupHost(int year, string city)
        {
            switch (year)
            {
                case 1930: return "Uruguay";
                case 1934: return "Italy";
                case 1938: return "France";
                case 1950: return "Brazil";
                case 1954: return "Switzerland";
                case 1958: return "Sweden";
                case 1962: return "Chili";
                case 1966: return "England";
                case 1970: return "Mexico";
                case 1974: return "Germany FR";
                case 1978: return "Argentina";
                case 1982: return "Spain";
                case 1986: return "Mexico";
                case 1990: return "Italy";
                case 1994: return "USA";
                case 1998: return "France";
                case 2002: return JapanOrKorea(city);
                case 2006: return "Germany";
                case 2010: return "South Africa";
                case 2014: return "Brazil";
                default: return "";
            }
        }

        //Info about world cup 2002 country
        private static string JapanOrKorea(string city)
        {
            string[] KoreaCities2002 = { "Seoul", "Ulsan", "Busan", "Gwangju", "Suwon", "Daegu", "Jeonju", "Jeju", "Incheon", "Daejeon" };
            foreach (string koreaCity in KoreaCities2002)
            {
                if (city.Contains(koreaCity)) return "South Korea";
            }
            return "Japan";
        }

        //Parse str date to three ints
        private static (int, int, int) StrToDateTime(string strDat)
        {
            string day, month, year;
            day = month = year = string.Empty;
            int i = 0;
            do
            {
                day += strDat[i];
                i++;
            } while (Char.IsDigit(strDat[i]) && i < strDat.Length);
            do
            {
                month += strDat[i];
                i++;
            } while (Char.IsLetter(strDat[i]) && i < strDat.Length);
            do
            {
                year += strDat[i];
                i++;
            } while (Char.IsDigit(strDat[i]) && i < strDat.Length);
            return (Convert.ToInt32(year.Trim()), MonthToInt(month.Trim()), Convert.ToInt32(day.Trim()));
        }
    }
}
