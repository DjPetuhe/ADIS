using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Adis_FirstLab
{
    public class Assistant
    {
        [Required]
        [MaxLength(50)]
        public string AssitantName { get; set; }
        [Key]
        public int AssistantID { get; set; }

        //Navigation property

        public ICollection<Fact_Matches> FirstAssistants { get; set; }
        public ICollection<Fact_Matches> SecondAssistants { get; set; }
    }
}
