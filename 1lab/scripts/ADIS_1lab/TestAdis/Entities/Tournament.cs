using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Tournament
    {
        [Required]
        [MaxLength(50)]
        public string TournamentName { get; set; }
        [Key]
        public int TournamentID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> Match_Tournament { get; set; }
    }
}
