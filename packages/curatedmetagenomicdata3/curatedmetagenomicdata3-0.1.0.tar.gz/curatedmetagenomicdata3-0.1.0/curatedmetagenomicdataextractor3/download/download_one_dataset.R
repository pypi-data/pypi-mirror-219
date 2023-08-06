library("curatedMetagenomicData")
library("stringr")
library("ExperimentHub")

args <- commandArgs()
saveDirectory <- args[6]
name <- args[7]
dryrun = FALSE

print(paste("Downloading files from curatedMetagenomicData to ", saveDirectory))
source("curatedmetagenomicdataextractor/download/download_utils.R")

names = getExperimentNames()

tryCatch ({
experiment = curatedMetagenomicData(name, dryrun = dryrun) |> mergeData()
# Write metagenomic data
saveFile = paste(saveDirectory, paste0(name,'.csv'), sep="/")
print(paste0('Writing: ', name,' to ', saveFile))    
saveObject = as.matrix(assay(experiment))
write.csv(saveObject, saveFile)
},
error = function(e) {print(paste("Failed to write CSVs for ", name))}
)

print(paste("Wrote CSVs from curatedMetagenomicData to ", saveDirectory))