# Description
Command line Python program to extract army rules and unit cards from 10th edition Warhammer 40k indexes to create army list specific pdfs with reduced file size. Requires Python and pypdf.

# Instructions
- Download an army index https://www.warhammer-community.com/warhammer-40000-downloads/#indexes-faqs-and-errata  
- Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- Install py40kie using pip:  
  ```
  pip install py40kie
  ```
- Run py40kie using command line:  
  ```
  py40kie [-h] [-o OUTPUT_PDF] [-a ARMY_RULES_PAGES [ARMY_RULES_PAGES ...]] [-v] index_pdf pages [pages ...]
  ```
  ###### Postional arguments
    - The "index.pdf" file to extract cards from  
    - Space separated list of cards to extract. Can be page numbers or **exact** unit titles. Army rules, strategems and unit wargear are included automatically  
    ###### Optional arguments:  
    - -o: The file to save the extracted pdf to. Folder path can be included  
    - -a: Optional argument to specify army rules and strategem pages (space separated numbers). Use this if the army rules and strategems are not contained in the first 4 pages of the index  
    - -v: Optional flag to override page extraction. Will extract only the page numbers specified  
  ### Examples  
  ```
  py40kie "tyranids index.pdf" 9 21 25 27 -o "my army list"  
  ```
  ```
  py40kie "tyranids index.pdf" "hive tyrant" "tyranid warriors with ranged bio-weapons" 25 "hOrMaGaUnTs" -o "./my lists/my army list"
  ```

# Contributions  
## Future features  
Any suggested features would be appreciated.  

## Issues  
py40kie was not tested on all indexes. If there is any problem extracting cards please submit an issue https://github.com/Dragons-Ire/40k-index-pdf-extractor/issues/new