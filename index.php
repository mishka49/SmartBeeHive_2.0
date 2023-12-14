    <?php
    $numbers = array();
    for ($i = 0; $i < 25; $i++) {
    $numbers[] = rand(10, 100);
    }

    sort($numbers);

    file_put_contents('numbers.txt', implode(';', $numbers));

    $numbers_string = file_get_contents('numbers.txt');
    $numbers = explode(';', $numbers_string);

    echo '<table style="border-collapse: collapse; border: 1px solid black;">';
    foreach ($numbers as $key=>$number) {
    echo '<tr><td style="border: 1px solid black; padding: 5px;">' . $number . '</td></tr>';
    }
    echo '</table>';
    ?>

