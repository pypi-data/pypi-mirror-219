from time import sleep

import os
from tkinter import Tk, filedialog
import xml.etree.ElementTree as ElementTree
import PySimpleGUI as psg
from xml.dom import minidom

import pytz
import datetime


def cria_unificado():
    root_unificado = ElementTree.Element("timetable", ascttversion="2021.6.2", importtype="database",
                                         options="export:idprefix:%CHRID,import:idprefix:%TEMPID,groupstype1,decimalseparatordot,lessonsincludeclasseswithoutstudents,handlestudentsafterlessons",
                                         defaultexport="1", displayname="aSc Timetables 2012 XML", displaycountries="")

    # tag periods
    periods = ElementTree.SubElement(root_unificado, "periods", options="canadd,export:silent",
                                     columns="period,name,short,starttime,endtime")

    ElementTree.SubElement(periods, "period", name="07:05", short="07:05", period="1", starttime="7:05", endtime="7:50")
    ElementTree.SubElement(periods, "period", name="07:50", short="07:50", period="2", starttime="7:50", endtime="8:35")
    ElementTree.SubElement(periods, "period", name="08:35", short="08:35", period="3", starttime="8:35", endtime="9:20")
    ElementTree.SubElement(periods, "period", name="09:40", short="09:40", period="4", starttime="9:40",
                           endtime="10:25")
    ElementTree.SubElement(periods, "period", name="10:25", short="10:25", period="5", starttime="10:25",
                           endtime="11:10")
    ElementTree.SubElement(periods, "period", name="11:10", short="11:10", period="6", starttime="11:10",
                           endtime="11:55")
    ElementTree.SubElement(periods, "period", name="11:55", short="11:55", period="7", starttime="11:55",
                           endtime="12:40")
    ElementTree.SubElement(periods, "period", name="12:40", short="12:40", period="8", starttime="12:40",
                           endtime="13:25")
    ElementTree.SubElement(periods, "period", name="13:25", short="13:25", period="9", starttime="13:25",
                           endtime="14:10")
    ElementTree.SubElement(periods, "period", name="14:10", short="14:10", period="10", starttime="14:10",
                           endtime="14:55")
    ElementTree.SubElement(periods, "period", name="15:15", short="15:15", period="11", starttime="15:15",
                           endtime="16:00")
    ElementTree.SubElement(periods, "period", name="16:00", short="16:00", period="12", starttime="16:00",
                           endtime="16:45")
    ElementTree.SubElement(periods, "period", name="16:45", short="16:45", period="13", starttime="16:45",
                           endtime="17:30")
    ElementTree.SubElement(periods, "period", name="17:30", short="17:30", period="14", starttime="17:30",
                           endtime="18:15")
    ElementTree.SubElement(periods, "period", name="18:15", short="18:15", period="15", starttime="18:15",
                           endtime="19:00")
    ElementTree.SubElement(periods, "period", name="19:00", short="19:00", period="16", starttime="19:00",
                           endtime="19:45")
    ElementTree.SubElement(periods, "period", name="19:45", short="19:45", period="17", starttime="19:45",
                           endtime="20:30")
    ElementTree.SubElement(periods, "period", name="20:45", short="20:45", period="18", starttime="20:45",
                           endtime="21:30")
    ElementTree.SubElement(periods, "period", name="21:30", short="21:30", period="19", starttime="21:30",
                           endtime="22:15")
    ElementTree.SubElement(periods, "period", name="22:15", short="22:15", period="20", starttime="22:15",
                           endtime="23:00")

    # tag daysdef
    daysdefs = ElementTree.SubElement(root_unificado, "daysdefs", columns="id,days,name,short")
    ElementTree.SubElement(daysdefs, "daysdef", id="6B3F12A34D97076A", name="Qualquer dia", short="X",
                           days="1000000,0100000,0010000,0001000,0000100,0000010,0000001")
    ElementTree.SubElement(daysdefs, "daysdef", id="805BDEBDA010C1F2", name="Cada dia", short="E", days="1111111")
    ElementTree.SubElement(daysdefs, "daysdef", id="A8F237B2F9E6B675", name="Segunda-feira ", short="Seg",
                           days="1000000")
    ElementTree.SubElement(daysdefs, "daysdef", id="CAB97D0425BEC0DA", name="Terça-feira", short="Ter", days="0100000")
    ElementTree.SubElement(daysdefs, "daysdef", id="60850D9314471122", name="Quarta-feira ", short="Qua",
                           days="0010000")
    ElementTree.SubElement(daysdefs, "daysdef", id="DDF4362F91A753AB", name="Quinta-feira ", short="Qui",
                           days="0001000")
    ElementTree.SubElement(daysdefs, "daysdef", id="E87DBCE4E7616290", name="Sexta-feira ", short="Sex", days="0000100")
    ElementTree.SubElement(daysdefs, "daysdef", id="23651B657C8E30B9", name="Sábado ", short="Sáb", days="0000010")
    ElementTree.SubElement(daysdefs, "daysdef", id="0E5CEC8F57D233C2", name="Horário Flutuante", short="Flutuante",
                           days="0000001")

    # tag weeksdef
    weeksdefs = ElementTree.SubElement(root_unificado, "weekdefs", options="canadd,export:silent",
                                       columns="id,weeks,name,short")
    ElementTree.SubElement(weeksdefs, "weekdef", id="4D751412E50EC8F8", name="Todas as semanas", short="Todas",
                           weeks="1")

    # tag termsdefs
    termsdefs = ElementTree.SubElement(root_unificado, "termsdefs", options="canadd,export:silent",
                                       columns="id,terms,name,short")
    ElementTree.SubElement(termsdefs, "termsdefs", id="402E718B0AFD874E", name="Todo o ano", short="ANO", terms="1")

    # tag subjects
    ElementTree.SubElement(root_unificado, "subjects", options="canadd,export:silent",
                           columns="id,name,short,partner_id")
    # tag teachers
    ElementTree.SubElement(root_unificado, "teachers", options="canadd,export:silent",
                           columns="id,name,short,gender,color,email,mobile,partner_id,firstname,lastname")

    # tag buildings
    ElementTree.SubElement(root_unificado, "buildings", options="canadd,export:silent",
                           columns="id,name,partner_id")

    # tag classrooms/ location
    ElementTree.SubElement(root_unificado, "classrooms", options="canadd,export:silent",
                           columns="id,name,short,capacity,buildingid,partner_id")

    # tag grades
    grades = ElementTree.SubElement(root_unificado, "grades", options="canadd,export:silent",
                                    columns="grade,name,short")
    for i in range(1, 21):
        ElementTree.SubElement(grades, "grade", name=f"Etapa {i}", short=f"Ano {i}", grade=f"{i}")

    # tag classes
    ElementTree.SubElement(root_unificado, "classes", options="canadd,export:silent",
                           columns="id,name,short,classroomids,teacherid,grade,partner_id")

    # tag groups
    ElementTree.SubElement(root_unificado, "groups", options="canadd,export:silent",
                           columns="id,classid,name,entireclass,divisiontag,studentcount,studentids")

    # tag students
    ElementTree.SubElement(root_unificado, "students", options="canadd,export:silent",
                           columns="id,classid,name,number,email,mobile,partner_id,firstname,lastname")

    # tag studentsubjects
    ElementTree.SubElement(root_unificado, "studentsubjects", options="canadd,export:silent",
                           columns="studentid,subjectid,seminargroup,importance,alternatefor")

    # tag lessons
    ElementTree.SubElement(root_unificado, "lessons", options="canadd,export:silent",
                           columns="id,subjectid,classids,groupids,teacherids,classroomids,periodspercard,periodsperweek,daysdefid,weeksdefid,termsdefid,seminargroup,capacity,partner_id")

    # tag cards
    ElementTree.SubElement(root_unificado, "cards", options="canadd,export:silent",
                           columns="lessonid,period,days,weeks,terms,classroomids")

    return root_unificado


def unifica_xml(root_unificado, root):
    # tag subjects
    # subjects = ElementTree.Element(root_unificado, "subject")
    for sub in root.iter("subject"):
        for child in root_unificado:
            tag = child.tag
            if tag == "subjects":
                ElementTree.SubElement(child, "subject", id=sub.get("id"), name=str(sub.get("name")),
                                       short=sub.get("short")
                                       , partner_id=sub.get("partner_id"))

    # tag teachers
    for tea in root.iter("teacher"):
        for child in root_unificado:
            tag = child.tag
            if tag == "teachers":
                ElementTree.SubElement(child, "teacher", id=tea.get("id"),
                                       firstname=tea.get("firstname"), lastname=tea.get("lastname")
                                       , name=tea.get("name"), short=tea.get("short"), gender=tea.get("gender"),
                                       color=tea.get("color"), email=tea.get("email"), mobile=tea.get("mobile"),
                                       partner_id=tea.get("partner_id"))

    # tag classroom
    for cla in root.iter("classroom"):
        for child in root_unificado:
            tag = child.tag
            if tag == "classrooms":
                ElementTree.SubElement(child, "classroom", id=cla.get("id"),
                                       name=cla.get("name"), short=cla.get("short"), capacity=cla.get("capacity"),
                                       buildingid=cla.get("buildingid"),
                                       partner_id=cla.get("partner_id"))

    # tag class
    for clas in root.iter("class"):
        for child in root_unificado:
            tag = child.tag
            if tag == "classes":
                ElementTree.SubElement(child, "class", id=clas.get("id"), name=clas.get("name"),
                                       short=clas.get("short"), teacherid="", classroomids="",
                                       grade="", partner_id=clas.get("partner_id"))

    for clas in root.iter("class"):
        for child in root_unificado:
            tag = child.tag
            if tag == "classes":
                ElementTree.SubElement(child, "class", id=clas.get("id"), name=clas.get("name"),
                                       short=clas.get("short"), teacherid="", classroomids="",
                                       grade="", partner_id=clas.get("partner_id"))

    for gro in root.iter("group"):
        for child in root_unificado:
            tag = child.tag
            if tag == "groups":
                ElementTree.SubElement(child, "group", id=gro.get("id"),
                                       name=gro.get("name"), classid=gro.get("classid"),
                                       studentids=gro.get("studentids"),
                                       entireclass=gro.get("entireclass"), divisiontag=gro.get("divisiontag"),
                                       studentcount=gro.get("studentcount"))

    for les in root.iter("lesson"):
        for child in root_unificado:
            tag = child.tag
            if tag == "lessons":
                ElementTree.SubElement(child, "lesson", id=les.get("id"),
                                       classids=les.get("classids"),
                                       subjectid=les.get("subjectid"),
                                       periodspercard=les.get("periodspercard"),
                                       periodsperweek=les.get("periodsperweek"),
                                       teacherids=les.get("teacherids"),
                                       classroomids=les.get("classroomids"),
                                       groupids=les.get("groupids"),
                                       capacity=les.get("capacity"),
                                       seminargroup=les.get("seminargroup"),
                                       termsdefid=les.get("termsdefid"),
                                       weeksdefid=les.get("weeksdefid"),
                                       daysdefid=les.get("daysdefid"), partner_id=les.get("partner_id"))

    for car in root.iter("card"):
        for child in root_unificado:
            tag = child.tag
            if tag == "cards":
                ElementTree.SubElement(child, "card", lessonid=car.get("lessonid"),
                                       classroomids=car.get("classroomids"),
                                       period=car.get("period"),
                                       terms=car.get("terms"),
                                       days=car.get("days"))

    return root_unificado


def corrige_caracteres_especiais(file_name):
    # Substitui o símbolo que causa erro
    # file_data = file_name.replace("&quot;", "").replace('& amp;','').replace(" &amp; ", "").replace(" ", "")
    file_data = file_name
    return file_data


def retira_flutuantes(root):
    list_id_flutantes = []
    # Itens que não podem ser apagados
    active_subjects = []
    active_teachers = []
    active_classrooms = []
    active_classes = []
    active_groups = []

    for day in root.iter("daysdef"):
        if day.get('name') == 'Horário Flutuante':
            id_flutuante = day.get('id')
            days_flutante = day.get('days')

    for car in root.iter("card"):
        if car.get('days') == days_flutante:
            list_id_flutantes.append(car.get('lessonid'))

    # removendo o card
    for car in root.find("cards").findall("card"):
        if car.get("lessonid") in list_id_flutantes:
            root.find("cards").remove(car)

    # removendo a lesson
    for les in root.find("lessons").findall("lesson"):
        if les.get("id") in list_id_flutantes:
            root.find("lessons").remove(les)

    # pegando ids ativas
    for lesson in root.iter("lesson"):

        active_teachers += lesson.get("teacherids").split(",")
        active_groups += lesson.get("groupids").split(",")
        active_classrooms += lesson.get("classroomids").split(",")
        active_subjects += lesson.get("subjectid").split(",")

        count_classes = lesson.get("classids").count(',')

        if count_classes == 0:
            count_classes = 1
        else:
            count_classes += 1

        for posicao in range(0, count_classes):
            active_classes.append(lesson.get("classids").split(',')[posicao])

    # excluindo
    for classes in root.find("classes").findall("class"):
        if classes.get("id") not in active_classes:
            root.find("classes").remove(classes)

    for classroom in root.find("classrooms").findall("classroom"):
        if classroom.get('id') not in active_classrooms:
            root.find("classrooms").remove(classroom)

    for subject in root.find("subjects").findall("subject"):
        if subject.get("id") not in active_subjects:
            root.find("subjects").remove(subject)

    for teacher in root.find("teachers").findall("teacher"):
        if teacher.get("id") not in active_teachers:
            root.find("teachers").remove(teacher)

    for group in root.find("groups").findall("group"):
        if group.get("id") not in active_groups:
            root.find("groups").remove(group)

    return root


def main(caminho_pasta, caminho_aux):
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    dt_now = utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
    pasta_raiz = caminho_pasta

    root_unificado = cria_unificado()
    tree = ""
    # Para cada diretório dentro do diretório raiz
    for dirpath, dirnames, filenames in os.walk(pasta_raiz):
        # dirpath =  caminho

        for file in filenames:
            file = file.upper()
            if not file.__contains__("XML"):
                continue

            # criando o xml que vai passar os dados
            file_name_xml = dirpath + "/" + file
            tree_xml = ElementTree.parse(file_name_xml)
            root = tree_xml.getroot()
            # unificando
            tree = unifica_xml(root_unificado, root)

        tree_sem_flutuantes = retira_flutuantes(tree)

        xml_string_sem_flutuantes = minidom.parseString(
            ElementTree.tostring(tree_sem_flutuantes, encoding="windows-1252")).toprettyxml(indent="   ")
        xml_string = minidom.parseString(ElementTree.tostring(tree, encoding="windows-1252")).toprettyxml(indent="   ")

        # forçar a mudança do enconding
        # contar quantas vezes o ? se repete para que na segunda vez sobreescreva o enconding correto
        posicao = 0
        contagem = 0
        lista = list(xml_string)
        for i in xml_string:
            if i == "?":
                contagem += 1
            if contagem == 2:
                contagem = 3
                lista[posicao] = "encoding='windows-1252'?"

            posicao += 1
        xml_string = "".join(lista)

        # forçar a mudança do enconding
        # contar quantas vezes o ? se repete para que na segunda vez sobreescreva o enconding correto
        posicao = 0
        contagem = 0
        lista = list(xml_string_sem_flutuantes)
        for i in xml_string_sem_flutuantes:
            if i == "?":
                contagem += 1
            if contagem == 2:
                contagem = 3
                lista[posicao] = "encoding='windows-1252'?"

            posicao += 1
        xml_string_sem_flutuantes = "".join(lista)

        name = f"{caminho_aux}/XML/XML_unificado_{str(dt_now.strftime('%y-%m-%d %H-%M'))}.xml"
        with open(name, "w", encoding="windows-1252") as f:
            xml_string = corrige_caracteres_especiais(xml_string)
            f.write(xml_string)

        return name


if __name__ == '__main__':
    main()
