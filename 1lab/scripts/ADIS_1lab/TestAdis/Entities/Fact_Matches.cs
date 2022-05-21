using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Adis_FirstLab
{
    public class Fact_Matches
    {
        public int? FirstTeamID { get; set; }
        public int? SecondTeamID { get; set; }
        public int? LocationID { get; set; }
        public int? DateID { get; set; }
        public int? RefereeID { get; set; }
        public int? FirstAssistantID { get; set; }
        public int? SecondAssistantID { get; set; }
        public int? TournamentID { get; set; }
        [Required]
        public int FirstTeamScore { get; set; }
        [Required]
        public int SecondTeamScore { get; set; }
        public bool neutral { get; set; }
        [Required]
        public bool Woomans { get; set; }
        [Key]
        public int ID { get; set; }

        //Navigation property

        public virtual Team FirstTeam { get; set; }
        public virtual Team SecondTeam { get; set; }
        [ForeignKey("LocationID")]
        public virtual Location Location { get; set; }
        [ForeignKey("DateID")]
        public virtual Date Date { get; set; }
        [ForeignKey("RefereeID")]
        public virtual Referee Referee { get; set; }
        public virtual Assistant FirstAssistnant { get; set; }
        public virtual Assistant SecondAssistant { get; set; }
    }
}
