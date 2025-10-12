---
layout: single
title: "Setting Up Simulations in R"
permalink: /simulator/
author_profile: false
description: "Full notebook from the expert panel session comparing R simulation frameworks for methodological studies."
---

{% include base_path %}

> Collaboration between Julie Aubert, Caroline Cognot, Annaïg De Walsche, Cédric Midoux, Pierre Neuvial, Aymeric Stamm, and Florian Teste.

## Overview

We explore several R packages for structuring simulation studies. Most simulation workflows follow three steps: generate data, run one or several methods, and compare results. The comparison below focuses on tools that streamline those steps for large-scale methodological research.

### Packages evaluated

- **simulator** — framework for streamlined simulations in methodological statistics, described in Bien (2016), *The simulator: An Engine to Streamline Simulations*.
- **simpr** — tidyverse-friendly framework for simulation, design analysis, and power analysis pipelines without verbose loops.
- **DeclareDesign** — focused on experimental design declaration and diagnosis; useful for design evaluation rather than method benchmarking.
- **MonteCarlo** — simplifies parameter grid loops and parallel Monte Carlo repetitions with LaTeX-ready outputs.
- **simChef** — low-code grammar for distributed simulations, producing interactive documentation that pairs results with reproducible workflows.
- **SimEngine** — provides structure for maintaining, running, and debugging simulations locally or on clusters with robust logging.

### Comparison snapshot

| Package | Version | Dependencies | Reverse deps | Latest commit | Latest release | CRAN | Primary maintainers |
|---------|---------|--------------|--------------|---------------|----------------|------|---------------------|
| [DeclareDesign](https://declaredesign.org/r/declaredesign/) | 1.0.10 | 2 | 1 | 2024-04-13 | 2024-04-21 | ✅ | Graeme Blair et al. |
| [MonteCarlo](https://github.com/FunWithR/MonteCarlo) | 1.0.6 | 6 | 0 | 2019-01-31 | 2019-01-31 | ✅ | Christian Hendrik Leschinski |
| [simChef](https://yu-group.github.io/simChef/index.html) | 0.1.0 | 22 | 0 | 2024-03-20 | – | ❌ | Tiffany Tang, James Duncan |
| [SimEngine](https://cran.r-project.org/web/packages/SimEngine/vignettes/SimEngine.html) | 1.4.0 | 6 | 0 | 2024-04-13 | 2024-04-04 | ✅ | Avi Kenny, Charles Wolock |
| [simpr](https://statisfactions.github.io/simpr/) | 0.2.6 | 11 | 0 | 2024-07-16 | 2023-04-26 | ✅ | Ethan Brown |
| [simulator](https://jacobbien.github.io/simulator/) | 0.2.5 | 1 | 0 | 2023-02-02 | 2023-02-04 | ✅ | Jacob Bien |

The only actively maintained package not on CRAN is **simChef**. Conversely, **MonteCarlo** shows limited recent activity. **DeclareDesign** targets experimental design evaluation rather than comparative method benchmarking, so the remainder of this notebook focuses on **SimEngine**, **simChef**, **simpr**, and **simulator**.

## Simulation use case: power curves for test calibration

We consider a paired two-sample *t*-test and estimate power across varying effect sizes (`mean_diff`), standard deviations (`sd`), and sample sizes (`n ∈ {100, 150, 200}`). Each package generates synthetic datasets, applies the statistical test, and aggregates rejection rates across repetitions to produce the power curve.

```r
# example scaffold (abbreviated)
library(ggplot2)
library(simulator)
library(simpr)
library(simChef)
library(SimEngine)

simulate_power <- function(n, sd, mean_diff, reps = 500) {
  replicate(reps, {
    x <- rnorm(n, mean = 0, sd = sd)
    y <- rnorm(n, mean = mean_diff, sd = sd)
    t.test(x, y, paired = TRUE)$p.value < 0.05
  })
}
```

Parameter grid used in the comparison:

- `n`: 100, 150, 200  
- `mean_diff`: 10, 20, 30  
- `sd`: 50, 100  

Power is estimated by simulating the paired *t*-test for each combination and repeating the simulation 10 times.

## Base R baseline

```r
## Set up parameters
ns <- c(100L, 150L, 200L)
mean_diffs <- c(10, 20, 30)
sds <- c(50, 100)
reps <- 10L

## Bring together into data frame
results_template <- expand.grid(
  n = ns, 
  mean_diff = mean_diffs, 
  sd = sds, 
  p.value = NA_real_
)
base_r_sim <- results_template[rep(1:nrow(results_template), each = reps), ]

## Loop over rows of the data frame and calculate the p-value
for (i in 1:nrow(results_template)) {
  params <- base_r_sim[i,]
  pre <- rnorm(params$n, 0, params$sd)
  post <- pre + rnorm(params$n, params$mean_diff, params$sd)
  base_r_sim$p.value[i] <- t.test(pre, post)$p.value
}

## Display table output
DT::datatable(base_r_sim)
```

The rest of the notebook positions each package relative to this baseline.

## simpr

### Issues with the baseline

According to the **simpr** authors the base R loop hides the important pieces of the simulation, makes error handling and parallelisation difficult, and is hard to read without extensive comments.

### simpr solution

```r
simpr_tbl <- specify(
  pre  = ~ rnorm(n, 0, sd),
  post = ~ pre + rnorm(n, mean_diff, sd)
) |> 
  define(n = ns, mean_diff = mean_diffs, sd = sds) |> 
  generate(reps, .progress = TRUE) |> 
  fit(t = ~ t.test(post, pre, paired = TRUE)) |> 
  tidy_fits()

DT::datatable(simpr_tbl)

simpr_tbl |> 
  dplyr::group_by(n, mean_diff, sd) |> 
  dplyr::summarize(Power = mean(p.value < 0.05)) |> 
  dplyr::ungroup() |> 
  ggplot(aes(n, Power)) + 
  geom_col() + 
  facet_grid(rows = dplyr::vars(sd), cols = dplyr::vars(mean_diff)) + 
  theme_bw()
```

### Philosophy

The workflow mirrors **infer**: `specify()` data generation, `define()` varying parameters, `generate()` data, `fit()` models, and `tidy_fits()` to consolidate results.

### Reproducible workflows

Same seeds reproduce results, and users can regenerate a specific subset for debugging.

```r
withr::with_seed(500, {
  specify(a = ~ runif(6)) |> 
    generate(3) |> 
    dplyr::filter(.sim_id == 3)
})
```

```r
withr::with_seed(500, {
  specify(a = ~ runif(6)) |> 
    generate(3, .sim_id == 3)
})
```

Benchmarking regenerating all simulations versus a subset:

```r
bench::mark(
  all = specify(a = ~ runif(6)) |> 
    generate(1000) |> 
    dplyr::filter(.sim_id == 1000),
  subset = specify(a = ~ runif(6)) |> 
    generate(1000, .sim_id == 1000),
  check = FALSE, min_iterations = 10L, relative = TRUE
)
```

#### Data munging per simulation

```r
#| eval: false
specify(
  pre  = ~ rnorm(n, 0, sd), 
  post = ~ pre + rnorm(n, mean_diff, sd)
) |> 
  define(n = ns, mean_diff = mean_diffs, sd = sds) |> 
  generate(reps, .progress = TRUE) |> 
  per_sim() |> 
  dplyr::mutate(dplyr::across(dplyr::everything(), dplyr::case_when(
    pre >  100 ~ 100,
    pre < -100 ~ -100,
    .default   ~ pre
  ))) |> 
  fit(t = ~ t.test(post, pre, paired = TRUE)) |> 
  tidy_fits()
```

#### Error handling

Simpr lets users configure whether errors stop, skip, or continue simulations, with hooks for debugging.

#### Parallelisation

```r
#| eval: false
library(future)
plan(multisession, workers = 6)
```

### Pros

- Tidyverse friendly and beginner accessible.  
- Built-in reproducibility, error handling, and parallelisation.  
- General-purpose for arbitrary R code.

### Cons

- Not the fastest option.  
- Less specialised than DeclareDesign.  
- No automatic reporting beyond what the user codes.

## simulator

### Getting started

`create()` scaffolds a project directory containing model, method, evaluation, and write-up templates.

```r
simulator_dir <- "./sims_simulator"
if (!file.exists(simulator_dir))
  create(simulator_dir)

withr::with_dir(simulator_dir, {
  list.files()
})
```

Template contents include:

- `model_functions.R` — define models with `new_model()`  
- `method_functions.R` — specify methods via `new_method()`  
- `eval_functions.R` — metrics with `new_metric()`  
- `main.R` — orchestrates the simulation

Example model definition:

```r
#| eval: false
make_my_model <- function(n, prob) {
  new_model(
    name = "contaminated-normal", 
    label = sprintf("Contaminated normal (n = %s, prob = %s)", n, prob), 
    params = list(n = n, mu = 2, prob = prob), 
    simulate = function(n, mu, prob, nsim) {
      contam <- runif(n * nsim) < prob
      x <- matrix(rep(NA, n * nsim), n, nsim)
      x[contam] <- rexp(sum(contam))
      x[!contam] <- rnorm(sum(!contam))
      x <- mu + x
      split(x, col(x))
    }
  )
}
```

Example method and metric definitions follow similarly.

Main script:

```r
#| eval: false
setwd(simulator_dir)

source("model_functions.R")
source("method_functions.R")
source("eval_functions.R")

name_of_simulation <- "normal-mean-estimation-with-contamination"

sim <- new_simulation(
  name = name_of_simulation,
  label = "Mean estimation under contaminated normal"
) %>%
  generate_model(
    make_model = make_my_model, 
    seed = 123,
    n = 50,
    prob = as.list(seq(0, 1, length = 6)),
    vary_along = "prob"
  ) %>%
  simulate_from_model(nsim = 10) %>%
  run_method(list(my_method, their_method)) %>%
  evaluate(list(his_loss, her_loss))

plot_eval_by(sim = sim, metric_name = "hisloss", varying = "prob")

tabulate_eval(
  object = sim, 
  metric_name = "herloss", 
  output_type = "markdown",
  format_args = list(digits = 1)
)
```

Power-curve example:

```r
#| warning: false
library(simulator)

source("simulator_equality_test/model_functions.R")
source("simulator_equality_test/method_functions.R")
source("simulator_equality_test/eval_functions.R")

name_of_simulation <- "normal-mean-test"

sim <- new_simulation(
  name = name_of_simulation, 
  label = "Test of mean"
) |> 
  generate_model(
    make_model = make_my_model_normal, 
    seed = 13, 
    n = 20, 
    mu2 = as.list(seq(0, 10, by = 0.5)), 
    mu1 = 0, 
    sig = 5, 
    vary_along = "mu2"
  ) |> 
  simulate_from_model(nsim = 1000) |> 
  run_method(list(t_test)) |> 
  evaluate(list(pval_loss))

tabulate_eval(
  sim, 
  metric_name = "p_value", 
  output_type = "markdown",
  format_args = list(digits = 5)
)

plot_eval_by(
  sim, 
  metric_name = "p_value", 
  varying = "mu2", 
  main = "Power curve with mu1=0 and varying mu2"
)
```

### Important functions

- `new_model()`, `new_method()`, `new_metric()`  
- `new_simulation()`, `generate_model()`, `simulate_from_model()`, `run_method()`, `evaluate()`  
- `plot_eval()`, `plot_eval_by()`, `tabulate_eval()`  

### Pros

- Supports any model the user can code.  
- Parameter iteration via pipelines.  
- Parallelisation possible through user choice of backend.  
- Stores all intermediate results in a tidy directory tree.

### Cons

- Requires adopting the package’s project structure.  
- Mixes template and user code.  
- Deep parameter grids may hit filesystem limits.

## SimEngine

Open-source R package for structuring simulations locally or on clusters, described in [Kenny & Wolock (2024)](https://arxiv.org/pdf/2403.05698).

### Example workflow

1. **Initialise**

```r
sim <- new_sim()
```

2. **Create generators**

```r
create_data <- function(n) {
  rpois(n = n, lambda = 20)
}

est_lambda <- function(dat, type) {
  if (type == "M") mean(dat)
  else if (type == "V") var(dat)
}
```

3. **Set simulation levels**

```r
sim <- sim |> 
  set_levels(
    estimator = c("M", "V"),
    n = c(10, 100, 1000)
  )
```

4. **Define the script**

```r
sim <- sim |> 
  set_script(function() {
    dat <- create_data(n = L$n)
    lambda_hat <- est_lambda(dat = dat, type = L$estimator)
    list("lambda_hat" = lambda_hat)
  })
```

5. **Configure and run**

```r
sim <- sim |> 
  set_config(
    num_sim = 100,
    packages = c("ggplot2", "stringr")
  )

sim <- run(sim)
```

6. **Summarise**

```r
sim |> 
  summarize(
    list(
      stat = "bias",
      name = "bias_lambda",
      estimate = "lambda_hat",
      truth = 20
    ), 
    list(
      stat = "mse",
      name = "mse_lambda",
      estimate = "lambda_hat",
      truth = 20
    )
  )
```

Inspect individual results:

```r
head(sim$results)
```

Update simulations with more replicates or level values:

```r
sim <- sim |> 
  set_config(num_sim = 200) |> 
  set_levels(
    estimator = c("M", "V"),
    n = c(10, 100, 1000, 10000)
  ) |> 
  update_sim()
```

### Parallelisation

Set `set_config(parallel = TRUE)` for parallel execution. Supports **local** mode (multiple cores on one machine) and **cluster** mode using `run_on_cluster()` with job scheduler integration (e.g. Slurm):

```r
run_on_cluster(
  first = {
    create_data <- function(n) rpois(n = n, lambda = 20)
    est_lambda <- function(dat, type) if (type == "M") mean(dat) else var(dat)
    sim <- new_sim() |> 
      set_levels(estimator = c("M", "V"), n = c(10, 100, 1000)) |> 
      set_script(function() {
        dat <- create_data(L$n)
        lambda_hat <- est_lambda(dat = dat, type = L$estimator)
        list("lambda_hat" = lambda_hat)
      }) |> 
      set_config(num_sim = 100, n_cores = 20)
  },
  main = {
    sim <- run(sim)
  },
  last = {
    sim <- summarize(sim)
  },
  cluster_config = list(js = "slurm")
)
```

### Pros

- Beginner friendly.  
- Works on local machines or clusters.  
- Excellent documentation and vignettes, including parallel-computing terminology.  
- Supports information sharing across simulation replicates and Monte Carlo error calculation.

### Cons

- Few drawbacks observed; performance depends on backend configuration.

## simChef

Simulation experiments are divided into four components: `DGP()`, `Method()`, `Evaluator()`, and `Visualizer()`. The package is not on CRAN and must be installed via GitHub.

### Setup

```r
#| eval: false
remotes::install_github("Yu-Group/simChef")
```

### Define components

```r
dgp_fun <- function(n, sd, mean_diff) {
  pre  <- rnorm(n, 0, sd)
  post <- pre + rnorm(n, mean_diff, sd)
  list(pre = pre, post = post)
}

method_fun <- function(pre, post) {
  t.test(post, pre, paired = TRUE)
}

evaluation_fun <- function(fit_results) {
  fit_results |> 
    dplyr::group_by(n, mean_diff, sd) |> 
    dplyr::summarize(Power = mean(p.value < 0.05))
}

power_plot_fun <- function(fit_results, eval_results) {
  fit_results |> 
    dplyr::group_by(n, mean_diff, sd) |> 
    dplyr::summarize(Power = mean(p.value < 0.05)) |> 
    ggplot(aes(n, Power)) + 
    geom_col() + 
    facet_grid(rows = dplyr::vars(sd), cols = dplyr::vars(mean_diff)) + 
    theme_bw()
}
```

### Convert to simChef classes

```r
dgp <- create_dgp(
  .dgp_fun = dgp_fun, .name = "DGP"
)

method <- create_method(
  .method_fun = method_fun, .name = "T-test"
)

evaluation <- create_evaluator(
  .eval_fun = evaluation_fun , .name = 'P.value'
)

power_plot <- create_visualizer(
  .viz_fun = power_plot_fun, .name = 'Power plot'
)
```

### Assemble and run experiment

```r
experiment <- create_experiment(name = "Example Experiment") |> 
  add_dgp(dgp) |> 
  add_method(method) |> 
  add_evaluator(evaluation) |> 
  add_visualizer(power_plot) |> 
  add_vary_across(.dgp = "DGP", n = ns, mean_diff = mean_diffs, sd = sds)

results <- run_experiment(experiment, n_reps = reps, save = TRUE)
DT::datatable(results$fit_results)
results$viz_results
```

### Pros

- Automated interactive documentation via `init_docs()` / `render_docs()`.  
- Easy parallelisation using `future::plan(multisession, workers = n_workers)`.  
- Flexible outputs; evaluation and visualisation can be rerun without refitting simulations by saving `fit_results`.

### Cons

- Not as fast as lower-level alternatives.  
- Only saves outputs from evaluation functions, making debugging harder.

## Summary of panel recommendations

| Framework | Best use case | Notes |
|-----------|---------------|-------|
| simpr | Rapid experimentation and tidy pipelines | Ideal for analysts comfortable with tidyverse idioms |
| simulator | Highly structured simulation projects | Requires adopting package’s directory template |
| SimEngine | Scalable experiments with audit trails | Excellent documentation and cluster support |
| simChef | Reproducible documentation with low code | Higher dependency footprint; GitHub-only |

## Download the Quarto source

The original Quarto notebook showcased during the panel is available for reference: [download `simulator.qmd`]({{ '/files/simulator.qmd' | relative_url }}).
