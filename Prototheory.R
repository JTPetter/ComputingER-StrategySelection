set.seed(123)
agent <- list("emotional_intensity" = 0,
              "desired_emotional_intensity" = 0,
              "choice_table" = data.frame("index" = 1:50,
                                          "intensity" = rep(0, 50),
                                          "expected_prob" = rep(0, 50),
                                          "prob_engage" = rep(.5, 50),
                                          "prob_disengage" = rep(.5, 50),
                                          "expect_reward_engage" = rep(-10, 50),
                                          "expect_reward_disengage" = rep(-10, 50),
                                          "previously_engaged" = rep(0, 50),
                                          "previous_encounters" = rep(0, 50)))
stimulus_probs <- sample(1:50, 50)
stimulus_weights <- stimulus_probs / sum(stimulus_probs)
world <- list("stimuli" = data.frame("index" = 1:50,
                                     "intensity" = sample(1:10, 50, replace = TRUE),
                                     "probs" = stimulus_weights))
#appraisal function
agent$choice_table$intensity <- world$stimuli$intensity
agent$choice_table$expected_prob <- world$stimuli$probs


repetitions <- 1000
learning_rate <- .01

for(r in 1:repetitions){
  print(paste(r/ (repetitions/100), "%"))
  
  currentStimulus <- sample(world$stimuli$index, 1, prob = world$stimuli$probs)
  
  #T1
  agent$emotional_intensity <- world$stimuli$intensity[world$stimuli$index == currentStimulus]
  #print(agent$emotional_intensity)
  reward_1 <- 10 - abs(agent$desired_emotional_intensity - agent$emotional_intensity)
  #print(reward_1)
  prob_for_stimuli <- subset(agent$choice_table, agent$choice_table$index == currentStimulus)
  strategy_choice <- sample(c("engage", "disengage"), 1, prob = c(prob_for_stimuli$prob_engage,
                                                                  prob_for_stimuli$prob_disengage))
  #print(strategy_choice)
  agent$choice_table$previous_encounters[currentStimulus] <- agent$choice_table$previous_encounters[currentStimulus] + 1
  
  #T2
  if (strategy_choice == "disengage") {
    agent$emotional_intensity <- agent$emotional_intensity * .5 
  } else if (strategy_choice == "engage"){
    if(agent$choice_table$previously_engaged[currentStimulus] == 0){
      agent$emotional_intensity <- agent$emotional_intensity * 1.1 
    } else {
      agent$emotional_intensity <- agent$emotional_intensity * .2
    }
    agent$choice_table$previously_engaged[currentStimulus] <- agent$choice_table$previously_engaged[currentStimulus] + 1
  }
  #print(agent$emotional_intensity)
  reward_2 <- 10 - abs(agent$desired_emotional_intensity - agent$emotional_intensity)
  #print(reward_2)
  
  #T3
  if (strategy_choice == "disengage") {
    agent$emotional_intensity <- agent$emotional_intensity * .5 
  } else if (strategy_choice == "engage"){
    agent$emotional_intensity <- agent$emotional_intensity * .5 
  }
  #print(agent$emotional_intensity)
  reward_3 <- 10 - abs(agent$desired_emotional_intensity - agent$emotional_intensity)
  #print(reward_3)
  
  #learning
  if (strategy_choice == "disengage") {
    total_reward_disengage <- sum(reward_1, reward_2, reward_3)
    updated_expectation <- mean(c(agent$choice_table$expect_reward_disengage[currentStimulus], total_reward_disengage))
    agent$choice_table$expect_reward_disengage[currentStimulus] <- updated_expectation
    if (total_reward_disengage > agent$choice_table$expect_reward_engage[currentStimulus]){ 
      agent$choice_table$prob_disengage[currentStimulus] <- (agent$choice_table$prob_disengage[currentStimulus] + learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
      agent$choice_table$prob_engage[currentStimulus] <- (agent$choice_table$prob_engage[currentStimulus] - learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
    } else {
      agent$choice_table$prob_disengage[currentStimulus] <- (agent$choice_table$prob_disengage[currentStimulus] - learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
      agent$choice_table$prob_engage[currentStimulus] <- (agent$choice_table$prob_engage[currentStimulus] + learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
    }
  } else if (strategy_choice == "engage"){
    total_reward_engage <- sum(reward_1, reward_2, reward_3)
    updated_expectation <- mean(c(agent$choice_table$expect_reward_engage[currentStimulus], total_reward_engage))
    agent$choice_table$expect_reward_engage[currentStimulus] <- updated_expectation
    if (total_reward_engage > agent$choice_table$expect_reward_disengage[currentStimulus]){ 
      agent$choice_table$prob_engage[currentStimulus] <- (agent$choice_table$prob_engage[currentStimulus] + learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
      agent$choice_table$prob_disengage[currentStimulus] <- (agent$choice_table$prob_disengage[currentStimulus] - learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
    } else {
      agent$choice_table$prob_engage[currentStimulus] <- (agent$choice_table$prob_engage[currentStimulus] - learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
      agent$choice_table$prob_disengage[currentStimulus] <- (agent$choice_table$prob_disengage[currentStimulus] + learning_rate) /
        sum(agent$choice_table$prob_disengage[currentStimulus], agent$choice_table$prob_engage[currentStimulus])
    }
  }
  agent$choice_table$prob_engage[currentStimulus] <- max(c(agent$choice_table$prob_engage[currentStimulus], 0))
  agent$choice_table$prob_engage[currentStimulus] <- min(c(agent$choice_table$prob_engage[currentStimulus], 1))
  agent$choice_table$prob_disengage[currentStimulus] <- max(c(agent$choice_table$prob_disengage[currentStimulus], 0))
  agent$choice_table$prob_disengage[currentStimulus] <- min(c(agent$choice_table$prob_disengage[currentStimulus], 1))
  
}


#choices over time, across all stimuli
ggplot2::ggplot(data = agent$choice_table) +
  ggplot2::geom_point(mapping = ggplot2::aes(x = previous_encounters, y = prob_engage)) +
  ggplot2::theme_light()

#choices in regard to intensity
ggplot2::ggplot(data = agent$choice_table) +
  ggplot2::geom_point(mapping = ggplot2::aes(x = intensity, y = prob_engage)) +
  ggplot2::theme_light()
