using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Adis_FirstLab
{
    public class WorldCupResults
    {
        public string Year { get; set; }
        public string Datetime { get; set; }
        public string Stage { get; set; }
        public string Stadium { get; set; }
        public string City { get; set; }
        [Column("Home Team Name")]
        public string Home_Team_Name { get; set; }
        [Column("Home Team Goals")]
        public int Home_Team_Goals { get; set; }
        [Column("Away Team Goals")]
        public int Away_Team_Goals { get; set; }
        [Column("Away Team Name")]
        public string Away_Team_Name { get; set; }
        [Column("Win conditions")]
        public string Win_conditions { get; set; }
        public int? Attendence { get; set; }
        [Column("Half-time Home Goals")]
        public int Half_time_Home_Goals { get; set; }
        [Column("Half-time Away Goals")]
        public int Half_time_Away_Goals { get; set; }
        public string Referee { get; set; }
        [Column("Assistant 1")]
        public string Assistant_1 { get; set; }
        [Column("Assistant 2")]
        public string Assistant_2 { get; set; }
        public int RoundID { get; set; }
        public int MatchID { get; set; }
        [Column("Home Team Initials")]
        public string Home_Team_Initials { get; set; }
        [Column("Away Team Initials")]
        public string Away_Team_Initials { get; set; }
        [Key]
        public int PK_WorldCupResults { get; set; }
    }
}
