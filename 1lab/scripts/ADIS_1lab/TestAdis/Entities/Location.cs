using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Location
    {
        [Required]
        [MaxLength(50)]
        public string CountryName { get; set; }
        [Required]
        [MaxLength(50)]
        public string City { get; set; }
        [MaxLength(50)]
        public string Stadium { get; set; }
        [Key]
        public int LocationID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> Match_Locations { get; set; }
    }
}
