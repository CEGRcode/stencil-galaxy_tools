#! /usr/bin/perl/

die "Input_File\tOutput_File\n" unless $#ARGV == 1;
my($input, $output) = @ARGV;
open(IN, "<$input") or die "Can't open $input for reading!\n";
open(OUT, ">$output") or die "Can't open $output for reading!\n";

print OUT "{\n";
print OUT "    \"compositePlot\": {\n";

print OUT "        \"title\": \"Composite Plot\",\n";
print OUT "        \"Xaxis\": \"";
$line = <IN>;
chomp($line);
@array = split(/\t/, $line);
shift(@array);
print OUT join(",", @array);
print OUT "\",\n";

print OUT "        \"Yaxis\": [\n";
print OUT "             {\n";
print OUT "                 \"title\": \"sampleSense\",\n";
print OUT "                 \"color\": \"0000FF\",\n";
print OUT "                 \"data\": \"";
$line = <IN>;
chomp($line);
@array = split(/\t/, $line);
shift(@array);
print OUT sprintf("%.4f", $array[0]);
for($x = 1; $x <= $#array; $x++) { print OUT ",",sprintf("%.4f", $array[$x]); }
print OUT "\"\n             },\n";

print OUT "             {\n";
print OUT "                 \"title\": \"sampleAnti\",\n";
print OUT "                 \"color\": \"FF0000\",\n";
print OUT "                 \"data\": \"";
$line = <IN>;
chomp($line);
@array = split(/\t/, $line);
shift(@array);
print OUT sprintf("%.4f", $array[0]);
for($x = 1; $x <= $#array; $x++) { print OUT ",",sprintf("%.4f", $array[$x]); }
print OUT "\"\n             }\n";
print OUT "        ]\n";
print OUT "    }\n";
print OUT "}\n";
close IN;
close OUT;
