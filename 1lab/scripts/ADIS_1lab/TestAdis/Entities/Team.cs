using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Team
    {
        [Required]
        [MaxLength(50)]
        public string TeamName { get; set; }
        [Key]
        public int TeamID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> FirstTeams { get; set; }
        public ICollection<Fact_Matches> SecondTeams { get; set; }
    }
}
