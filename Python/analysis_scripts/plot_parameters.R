# FUNCTIONS
.read_all_datasets <- function(file_path, file_numbers){
  all_datasets <- list()
  for (i in 1:length(file_numbers)) {
    file_name <- paste(file_path, file_numbers[i] , ".csv", sep = "")
    dataset <- as.data.frame(read.csv(file_name))
    dataset <- tidyr::gather(dataset, action, cumSum, inaction:engange, factor_key = TRUE)
    all_datasets[[i]] <- dataset
  }
  return(all_datasets)
}

.cum_sum_lineplots <- function(data_list, parameter){
  parameter_name <- deparse(substitute(parameter))
  for (i in 1:length(data_list)) {
    dataset <- data_list[[i]]
    plot_file_name <- paste(parameter_name, "_", parameter[i], ".png", sep = "")
    png(plot_file_name)
    plot <- ggplot2::ggplot() +
      ggplot2::geom_line(data = dataset, mapping = ggplot2::aes(x = X, y = cumSum, group = action, color = action), size = 1) +
      ggplot2::xlab("Time in runs") +
      ggplot2::ylab("Cum. Sum") +
      ggplot2::ggtitle(paste(parameter_name, "=", parameter[i], sep = "")) +
      ggplot2::theme_light()
    print(plot)
    dev.off()
  }
}



#N_RUNS

N_RUNS <- seq(1000, 8000, 1000)
path <- "../datasets/N_RUNS/N_RUNS"
all_N_RUNS <- .read_all_datasets(path, N_RUNS)
.cum_sum_lineplots(all_N_RUNS, N_RUNS)

#N_STIMULI
N_STIMULI <- seq(1000, 8000, 1000)
path <- "../datasets/N_STIMULI/N_STIMULI"

all_N_STIMULI <- .read_all_datasets(path, N_STIMULI)
.cum_sum_lineplots(all_N_STIMULI, N_STIMULI)


#Seed
seed <- 1:8
path <- "../datasets/Seed/Seed"

all_N_STIMULI <- .read_all_datasets(path, seed)
.cum_sum_lineplots(all_N_STIMULI, seed)





#engage_adaptation
engage_adapt <- seq(0, .8, .1)
path <- "../datasets/engage_adaptation/engage_adaptation_"

all_engage_adapt <- .read_all_datasets(path, engage_adapt)
.cum_sum_lineplots(all_engage_adapt, engage_adapt)




#no benefits
no_benefits <- ""
path <- "../datasets/no_benefits/no_benefits"
data_list <- .read_all_datasets(file_path = path, file_numbers = no_benefits)
.cum_sum_lineplots(data_list, no_benefits)


#no benefits but engage
no_benefits <- ""
path <- "../datasets/no_benefits/no_benefits_but_engage"
data_list <- .read_all_datasets(file_path = path, file_numbers = no_benefits)
.cum_sum_lineplots(data_list, no_benefits)

#no benefits but engage_no_delay
no_benefits <- ""
path <- "../datasets/no_benefits/no_benefits_but_engage_no_delay"
data_list <- .read_all_datasets(file_path = path, file_numbers = no_benefits)
.cum_sum_lineplots(data_list, no_benefits)

#no benefits but disengage
no_benefits <- ""
path <- "../datasets/no_benefits/no_benefits_but_disengage"
data_list <- .read_all_datasets(file_path = path, file_numbers = no_benefits)
.cum_sum_lineplots(data_list, no_benefits)

