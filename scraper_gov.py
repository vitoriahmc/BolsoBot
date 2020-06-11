from selenium import webdriver
browser = webdriver.Chrome(executable_path='./chromedriver.exe')
pages = 8
for i in range(1, pages):
    page = i
    if i == 1:
        browser.get(f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos')
    else:
        browser.get(f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos?b_start:int={(i-1) * 30}')

    speeches = browser.find_elements_by_tag_name('h2')
    j = 0
    while j < len(speeches):
        speeches = browser.find_elements_by_tag_name('h2')
        speech = speeches[j]
        link = speech.find_element_by_tag_name('a').get_attribute('href')
        browser.get(link)
        element = browser.find_element_by_id('parent-fieldname-text')
        text = element.text
        with open(f'./gov/file{j}{i}.txt', 'w', encoding='utf-8') as file:
            file.write(text)
            file.close()

        if i == 1:
            browser.get(f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos')
        else:
            browser.get(f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos?b_start:int={(i-1) * 30}')
        j += 1
        print(f'{(i/8 + (1/8 * j/len(speeches))) * 100}%', end='\r')
browser.close()


# python run_language_modeling.py  --output_dir='./output'  --model_type=gpt2  --save_total_limit=5  --num_train_epochs=1.0  --do_train  --logging_steps=500  --save_steps=500  --train_data_file=data.txt --model_name_or_path=gpt2-medium --block_size=128 --batch_size=256