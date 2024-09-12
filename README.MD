
# Python & Selenium პროექტი Rocky Linux-ზე

ეს პროექტი მოიცავს Selenium-ის, Telegram ბოტისა და Python-ის გამოყენებას. ქვემოთ მოცემულია ინსტრუქცია, თუ როგორ უნდა მართოთ პროექტი Rocky Linux-ზე.

## 1. Python-ის და ვირტუალური გარემოს დაყენება

დარწმუნდით, რომ სისტემაზე ინსტალირებულია Python 3.6 ან უფრო ახალი ვერსია.

### Python-ის ინსტალაცია:

```bash
sudo dnf install python3
```

### Python-ის ვერსიის შემოწმება:

```bash
python3 --version
```

### ვირტუალური გარემოს შექმნა და აქტივაცია:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### pip-ის განახლება:

```bash
pip install --upgrade pip
```

## 2. საჭირო ბიბლიოთეკების ინსტალაცია

პროექტის პაკეტების ინსტალაციისთვის გამოიყენეთ `requirements.txt` ფაილი:

```bash
pip install -r requirements.txt
```

## 3. Google Chrome და ChromeDriver-ის ინსტალაცია

Selenium-ის მართვისთვის საჭიროა Google Chrome და ChromeDriver.

### Google Chrome-ის ინსტალაცია:

დამატებითი რეპოზიტორიის გააქტიურება და Google Chrome-ის ინსტალაცია:

```bash
sudo dnf install fedora-workstation-repositories
sudo dnf config-manager --set-enabled google-chrome
sudo dnf install google-chrome-stable
```

### ChromeDriver-ის ინსტალაცია:

1. შეამოწმეთ თქვენი Google Chrome-ის ვერსია:

   ```bash
   google-chrome --version
   ```

2. გადმოწერეთ შესაბამისი ChromeDriver [აქედან](https://sites.google.com/a/chromium.org/chromedriver/downloads) თქვენი ბრაუზერის ვერსიის მიხედვით.

3. გადაადგილეთ `chromedriver` `/usr/local/bin` დირექტორიაში და მისცეთ შესაბამისი უფლებები:

   ```bash
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   ```

## 4. Selenium-ის კონფიგურაცია

პროექტის კონფიგურაციისთვის, უნდა მიუთითოთ თქვენი `chromedriver` ფაილის ადგილმდებარეობა. თუ `chromedriver` ინახება `/usr/local/bin/`-ში:

```python
chrome_driver_path = "/usr/local/bin/chromedriver"
```

## 5. Google Chrome-ის headless (ჩუმი) რეჟიმის გამოყენება

თქვენი სკრიპტი headless რეჟიმში რომ იმუშაოს (ბრაუზერის UI-ის გარეშე):

```python
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

## 6. Telegram Bot-ის კონფიგურაცია

1. მიიღეთ თქვენი ბოტის ტოკენი [BotFather](https://t.me/BotFather)-ის გამოყენებით.

2. ჩაწერეთ თქვენი ტოკენი და ჩატის ID თქვენს სკრიპტში:

```python
TOKEN = 'შენი ტოკენი'
CHAT_ID = 'შენი ჯგუფის ან მომხმარებლის ID'
```

## 7. პროექტის გაშვება

1. თუ ჯერ არ გაქვთ ვირტუალური გარემო გააქტიურებული, გააკეთეთ ეს:

   ```bash
   source myenv/bin/activate
   ```

2. სკრიპტის გაშვება:

   ```bash
   python3 შენი_სკრიპტი.py
   ```

## 8. სერვერის ფონზე გაშვება

თუ გსურთ, რომ სკრიპტი სერვერის ფონზე იმუშაოს, შეგიძლიათ გამოიყენოთ `nohup` ან `tmux`:

```bash
nohup python3 შენი_სკრიპტი.py &
```

## 9. პროდუქციის მონაცემების JSON ფაილში შენახვა

პროექტი მონაცემებს ინახავს `products.json` ფაილში, რომელიც შეიცავს ყველა აღრიცხულ პროდუქტს. დარწმუნდით, რომ ფაილი სწორად არის ჩატვირთული და ამუშავებული.

## 10. დამატებითი ინფორმაცია

- **ChromeDriver ვერსიების შესაბამისობა**: დარწმუნდით, რომ თქვენი Google Chrome-ის ვერსია შეესაბამება თქვენს ChromeDriver-ის ვერსიას.
- **pip პაკეტები**: შეგიძლიათ დაათვალიეროთ `requirements.txt` ფაილი საჭირო პაკეტების ინსტალაციისთვის.

## 11. requirements.txt

```txt
selenium==4.10.0
python-telegram-bot==20.0
asyncio==3.4.3
```

შენი პროექტი ახლა მზად არის სამუშაოდ Rocky Linux-ზე!
