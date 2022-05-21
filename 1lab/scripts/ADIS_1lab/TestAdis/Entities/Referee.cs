using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Referee
    {
        [Required]
        [MaxLength(50)]
        public string RefereeName { get; set; }
        [Key]
        public int RefereeID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> Match_Referees { get; set; }
    }
}
