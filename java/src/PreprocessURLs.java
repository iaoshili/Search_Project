import de.l3s.boilerpipe.extractors.ArticleExtractor;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Array;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.FileWriter;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 * Created by Greyjoy on 4/7/15.
 */
public class PreprocessURLs {
    private String writeToDirectoryPath;

    public PreprocessURLs(String writeToDirectoryPath) {
        this.writeToDirectoryPath = writeToDirectoryPath;
    }

    public void saveInfoInCategory(String category){
        int pageNum = 134;
        while (true) {
            String pageUrl = "http://www.theverge.com/"+category+"/archives/"+Integer.toString(pageNum);
            System.out.println("Fetching page: "+Integer.toString(pageNum) + " "+pageUrl);
            ArrayList<String> urls = getUrlsOfThisPage(pageUrl);
            if (urls.size() <= 1) {
                System.out.println("This category is exhausted.");
                break;
            }
            else {
                for (String url:urls) {
                    extractInfoFromUrlToJson(url);
                }
                pageNum ++;
            }
        }
    }

    private ArrayList<String> getUrlsOfThisPage(String url){
        Document doc = null;
        ArrayList<String> urls = new ArrayList<String>();

        try {
            doc = Jsoup.connect(url).get();
        }
        catch (IOException e ){
            System.out.println(e.toString());
        }
        catch (Exception e) {
            System.out.println(e.toString());
        }
        finally {
            Element tagArea = doc.select("div.m-tag-page__content").first();
            Elements resultLinks = tagArea.select("h3 a[href]");

            for (Element link:resultLinks){
                String linkStr = link.attr("href");
                urls.add(linkStr);
            }
        }

        return  urls;
    }

//    public void generateTokensFromFile() {
//        String filePath = urlFilePath;
//        String collegeAndItsUrlString = ProcessFile.readStringFromFile(filePath);
//        String[] collegeAndItsUrlList = collegeAndItsUrlString.split("\n");
//        for (int i = 23; i < collegeAndItsUrlList.length; i++) {
//            String collegeAndItsUrl = collegeAndItsUrlList[i];
//            String[] currentCollegeAndItsUrlInList = collegeAndItsUrl.split(" |\t");
//            int currentLineLength = currentCollegeAndItsUrlInList.length;
//            String collegeName = ListToString(currentCollegeAndItsUrlInList,0,currentLineLength-1);
//            String url = currentCollegeAndItsUrlInList[currentLineLength-1];
//
//            if (url.contains("pdf")) {
//                System.out.println(url+" temporarily not supported");
//                continue;
//            }
//            System.out.println("Feching "+url);
//
//            generateTokens(url, collegeName);
//        }
//    }

    //以后要处理这个方法的异常
    private static String ListToString(String[] strList, int startIndex, int endIndex) {
        StringBuffer result = new StringBuffer();
        for (int i = startIndex; i < endIndex; i++) {
            result.append(strList[i] + " ");
        }
        return result.toString();
    }

    public void generateTokens(String url, String collgeName) {
        URL almaMater = null;
        ArrayList<String> tokenList = null;

        try {
            almaMater = new URL(url);  // I went to Cinnaminson High School in New Jersey :)

        }
        catch (MalformedURLException e) {
            System.out.println(e.toString());
        }

        StringBuffer finalTextToBeLabeled = new StringBuffer();

//        String text = extractTextFromUrl(url);

        String tempFilePath = "/Users/Greyjoy/Desktop/temp";
//        ProcessFile.writeToFile(text,tempFilePath);
        try {
            tokenList = StanfordTokenizer.getTokensByToken(tempFilePath);
        }
        catch (IOException e) {
            System.out.println(e.toString());
        }

        for (String token : tokenList) {
            finalTextToBeLabeled.append(token+ " O" + "\n");
        }

        String filePath = writeToDirectoryPath+"/"+collgeName;
        ProcessFile.writeToFile(finalTextToBeLabeled.toString(),filePath);
    }

    private String getTitleFromUrl(String url) {
        Document doc = null;
        String title = null;

        try {
            doc = Jsoup.connect(url).get();
        }
        catch (IOException e ){
            System.out.println(e.toString());
        }
        catch (Exception e) {
            System.out.println(e.toString());
        }
        finally {
            title = doc.title();
        }
        return title;
    }

    private String getMainTextFromUrl(String urlStr) {
        String mainText = null;
        try {
            URL url = new URL(urlStr);
            mainText = ArticleExtractor.INSTANCE.getText(url);
        }
        catch (Exception e) {
            System.out.println(e.toString());
        }
        finally {
            //Intentionally do nothing here
        }
        return mainText;
    }

    private String[] getTagsFromUrl(String url) {
        String content = null;
        String[] tags = null;
        try {
            content = new Scanner(new URL(url).openStream(), "UTF-8").useDelimiter("\\A").next();
        }
        catch (MalformedURLException e){
            System.out.println(e.toString());
        }
        catch (IOException e) {
            System.out.println(e.toString());
        }
        catch (Exception e) {
            System.out.println(e.toString());
        }
        finally {
            Pattern p = Pattern.compile("front-page:(.*)\",\"Author\":");
            Matcher m = p.matcher(content);

            String tagStr = null;
            if (m.find()) {
                tagStr = m.group(1);
            }
            tags = tagStr.split(":");

        }
        return tags;
    }

    /**
     * Given a url from the verge.com. Save the interesting fields in json format to the specified output directory.
     * @param url
     */
    public void extractInfoFromUrlToJson(String url){
        String title = getTitleFromUrl(url);
        String mainText = getMainTextFromUrl(url);
        String[] tags = getTagsFromUrl(url);

        JSONObject obj = new JSONObject();
        obj.put("Main text", mainText);
        obj.put("Title", title);

        JSONArray tagArr = new JSONArray();
        for (String tag : tags) {
            tagArr.add(tag);
        }
        obj.put("Tags",tagArr);


        ProcessFile.writeToFile(obj.toJSONString(),writeToDirectoryPath+"/"+title);
    }

}

