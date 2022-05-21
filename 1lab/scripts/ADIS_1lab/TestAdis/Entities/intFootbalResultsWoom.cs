using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Adis_FirstLab
{
    [Table("intFootbalResultsWoom")]
    public class intFootbalResultsWoom
    {
        public System.DateTime date { get; set; }
        public string home_team { get; set; }
        public string away_team { get; set; }
        public int home_score { get; set; }
        public int away_score { get; set; }
        public string tournament { get; set; }
        public string city { get; set; }
        public string country { get; set; }
        public string neutral { get; set; }
        [Key]
        public int PK_intFootbalResults { get; set; }
    }
}
