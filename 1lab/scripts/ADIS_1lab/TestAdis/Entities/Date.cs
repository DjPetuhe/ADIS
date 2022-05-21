using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Date
    {
        [Required]
        public int Year { get; set; }
        [Required]
        public int Month { get; set; }
        [Required]
        public int Day { get; set; }
        [Key]
        public int DateID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> Match_Dates { get; set; }
    }
}
