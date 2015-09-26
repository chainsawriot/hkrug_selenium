require(rvest)
require(plyr)
require(dplyr)
require(stringr)

# Intro to Xpath
# find the first table tag

html('http://racing.hkjc.com/racing/Info/Meeting/VeterinaryRecord/English/Local/20150928/ST/1') %>% html_node(xpath = '//table')


# Find all table tags

html('http://racing.hkjc.com/racing/Info/Meeting/VeterinaryRecord/English/Local/20150928/ST/1') %>% html_nodes(xpath = '//table') %>% length

html('http://racing.hkjc.com/racing/Info/Meeting/VeterinaryRecord/English/Local/20150928/ST/1') -> hkjc

# Find table with specific attribute

hkjc %>% html_node(xpath = "//table[@class='tableBorder0 tdAlignL']")

hkjc %>% html_node(xpath = "//table[@class='tableBorder0 tdAlignL']") %>% html_table -> raw_table

colnames(raw_table) <- c("HorseNo", "HorseName", "Date", "Details", "Passon")
raw_table <- raw_table[2:nrow(raw_table),]

## remove rubbish

raw_table$HorseNo
str_trim(raw_table$HorseNo)
raw_table %>% mutate_each(funs(str_trim))

## http://pokemon.wikia.com/wiki/List_of_Pok%C3%A9mon

html("http://pokemon.wikia.com/wiki/List_of_Pok%C3%A9mon") %>% html_nodes(xpath = "//table[@class='wikitable sortable']") %>% html_table %>% do.call("rbind", .)

## Non-html table case

## metro mobile: http://www.metrohk.com.hk/pda/pda.php

html('http://www.metrohk.com.hk/pda/pda.php') -> metrohk

metrohk %>% html_nodes(xpath = "//div[contains(@class, 'newsItm')]") -> newsitems

## will not extract the first item

metrohk %>% html_nodes(xpath = "//div[contains(@class, 'newsItm')]") -> newsitems


metrohk %>% html_nodes(xpath = "//div[contains(@class, 'newsItm')] | //div[@class='firstArticle']") -> newsitems


newsitems %>% html_node('img')
newsitems %>% html_node('a') %>% html_attr('href')

extractnode <- function(node) {
    node %>% html_text -> title
    html_node(node, 'a') %>% html_attr('href') -> url
    html_node(node, 'img') %>% html_attr('src') -> imgsrc
    return(data_frame(title = title, url = url, img = imgsrc))
}

newsdf <- ldply(newsitems, extractnode)

html(paste0("http://www.metrohk.com.hk/pda/", newsdf$url[1])) %>% html_node(xpath = "//div[@class='cContent']") %>% html_nodes('p') %>% html_text %>% paste(collapse = " ") %>% str_trim

## pack that into a func

getnewscontent <- function(url) {
    html(paste0("http://www.metrohk.com.hk/pda/", url)) %>% html_node(xpath = "//div[@class='cContent']") %>% html_nodes('p') %>% html_text %>% paste(collapse = " ") %>% str_trim
}

full_text <- ldply(newsdf$url, getnewscontent, .progress = 'text')

complete_data <- cbind(newsdf, full_text)

write.csv(complete_data, "metro.csv")

5 -> hello
hello <- 6
