using System.Data.Entity;

namespace Adis_FirstLab
{
    public class footbal_StarEntities : DbContext
    {
        public footbal_StarEntities()
            : base("name=BloggingCompactDatabase")
        {
        }

        public virtual DbSet<intFootbalResults> intFootbalResults { get; set; }
        public virtual DbSet<intFootbalResultsWoom> intFootbalResultsWoom { get; set; }
        public virtual DbSet<WorldCupResults> WorldCupResults { get; set; }
        public virtual DbSet<Team> Team { get; set; }
        public virtual DbSet<Referee> Referee { get; set; }
        public virtual DbSet<Assistant> Assistant { get; set; }
        public virtual DbSet<Tournament> Tournament { get; set; }
        public virtual DbSet<Date> Date { get; set; }
        public virtual DbSet<Location> Location { get; set; }
        public virtual DbSet<Fact_Matches> Fact_Matches { get; set; }
        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Fact_Matches>()
                        .HasRequired(m => m.FirstTeam)
                        .WithMany(t => t.FirstTeams)
                        .HasForeignKey(m => m.FirstTeamID)
                        .WillCascadeOnDelete(false);
            modelBuilder.Entity<Fact_Matches>()
                        .HasRequired(m => m.SecondTeam)
                        .WithMany(t => t.SecondTeams)
                        .HasForeignKey(m => m.SecondTeamID)
                        .WillCascadeOnDelete(false);
            modelBuilder.Entity<Fact_Matches>()
                        .HasRequired(m => m.FirstAssistnant)
                        .WithMany(t => t.FirstAssistants)
                        .HasForeignKey(m => m.FirstAssistantID)
                        .WillCascadeOnDelete(false);
            modelBuilder.Entity<Fact_Matches>()
                        .HasRequired(m => m.SecondAssistant)
                        .WithMany(t => t.SecondAssistants)
                        .HasForeignKey(m => m.SecondAssistantID)
                        .WillCascadeOnDelete(false);
            modelBuilder.Entity<Fact_Matches>()
                        .Property(m => m.SecondAssistantID)
                        .IsOptional();
            modelBuilder.Entity<Fact_Matches>()
                        .Property(m => m.FirstAssistantID)
                        .IsOptional();
        }
    }
}
