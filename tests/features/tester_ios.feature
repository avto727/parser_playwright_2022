Feature: tester_ios
  schedule может принимать 3 значения
  удаленка, гибрид, удаленка+гибрид


  @tester_ios
  Scenario: tester_ios
    Given Open browser base_url keyword=ios schedule=удаленка step 1
    When click Button_Всё_верно step 2
    When determinate total_pages to store step 3
    When pages with list vacancy processing step 4
    When sort salary and delete doubles step 5
    When sort for plus words title save to sort_plus_title_ios step 6

    When sort for plus words description vacancy step 7