"""Simulate large CHIME population."""
from frbpoppy import CosmicPopulation, lognormal, Survey
from frbpoppy import SurveyPopulation, pprint

N_SRCS = 9e3
N_DAYS = 100
RATE = 9.5  # per day
# Chime started in Aug 2018. Assuming 2/day for one-offs.
# Total of 9 repeaters published on 9 Aug 2019. = ~year
N_CHIME = {'rep': 9, 'one-offs': 365*2, 'time': 365}

r = CosmicPopulation(N_SRCS, n_days=N_DAYS, repeaters=True)
r.set_dist(model='vol_co', z_max=1.0)
r.set_dm_host(model='gauss', mean=100, std=200)
r.set_dm_igm(model='ioka', slope=1000, std=None)
r.set_dm(mw=True, igm=True, host=True)
r.set_emission_range(low=100e6, high=10e9)
r.set_lum(model='powerlaw', per_source='different', low=1e40, high=1e45,
          power=0)
r.set_si(model='gauss', mean=-1.4, std=1)
r.set_w(model='lognormal', per_source='different', mean=0.1, std=1)
rate = lognormal(RATE, 1, int(N_SRCS))
r.set_time(model='poisson', rate=rate)

# Set up survey
s = Survey('chime', n_days=N_DAYS)
s.set_beam(model='chime')

# Only generate FRBs in CHIME's survey region
r.set_direction(model='uniform',
                min_ra=s.ra_min,
                max_ra=s.ra_max,
                min_dec=s.dec_min,
                max_dec=s.dec_max)

r.generate()

surv_pop = SurveyPopulation(r, s)
surv_pop.name = 'complex_chime'
surv_pop.save()

print(surv_pop.source_rate)
print(surv_pop.burst_rate)
pprint(f'# one-offs: {surv_pop.n_one_offs()}')
pprint(f'# repeaters: {surv_pop.n_repeaters()}')
