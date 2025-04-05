#!/usr/bin/php -q
<?php

echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMail');
if(date('Y-m-d')!=date('Y-m-d', strtotime('monday'))):
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/GetTndrDetail');
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/GetTndrinterDetail');
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/GetTndrResultById');
 
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/copytenderinfo');
  echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/copytendernational');
   echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/copytenderinternational');
   
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/Crontndrtwentyfournationalcsv');
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/Crontndrtwentyfourintercsv');
 // echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/NoGoList');
 echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/UpdateTenderOldExpiry');
 echo file_get_contents('http://103.210.112.132/bd/index.php/Testresult/tenderinfoxml');
  echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/Crontndrninfoxml');
 endif;

echo file_get_contents('http://103.210.112.132/bd/index.php/Tenderfilter_cron/cron');
echo file_get_contents('http://103.210.112.132/bd/index.php/Tenderfilter_cron/sectorcron');
echo file_get_contents('http://103.210.112.132/bd/index.php/Tenderfilter_cron/servicescron');
echo file_get_contents('http://103.210.112.132/bd/index.php/Tenderfilter_cron/croninrevieproject');

if(date('Y-m-d')==date('Y-m-d', strtotime('tuesday'))):
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingEOI_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingRFP_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingFQ_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedEOI_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedRFP_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedFQ_Data');
   // echo file_get_contents('https://hrms.cegindia.com/myhrms/index.php/CronMail_Controller/reminderOfProbationDays');
endif;

if(date('Y-m-d')==date('Y-m-d', strtotime('friday'))):
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingEOI_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingRFP_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailOngoingFQ_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedEOI_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedRFP_Data');
    echo file_get_contents('http://103.210.112.132/bd/index.php/CronJob_Controller/sendMailSubmittedFQ_Data');
   // echo file_get_contents('https://hrms.cegindia.com/myhrms/index.php/CronMail_Controller/reminderOfProbationDays');
endif;

?>